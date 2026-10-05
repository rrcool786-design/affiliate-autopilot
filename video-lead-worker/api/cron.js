const { MongoClient } = require('mongodb');

const MAX_AGE_DAYS = 14;
const MAX_SEEN = 800;
const LOCK_MS = 15 * 60 * 1000;
const STATE_KEY = 'video_lead_finder_v1';
const LOCK_KEY = 'video_lead_finder_lock_v1';

const STRONG = ['video editor','video editing','short-form video','short form video','shorts editor','reels editor','social video editor','ai video editor'];
const SUPPORT = ['youtube shorts','instagram reels','reels','short-form','short form','motion graphics','talking head','social media video','content editor','video producer'];
const TECH = ['ai ','artificial intelligence','saas','software','tech ','technology','startup','b2b'];
const CONTRACT = ['freelance','contract','project-based','project based','part-time','part time','retainer'];
const SENIOR = ['senior ','manager','director','head of','lead video'];
const LOC = ['worldwide','anywhere','global','india','asia','apac','remote'];

function plain(v=''){return String(v).replace(/<[^>]*>/g,' ').replace(/&nbsp;/gi,' ').replace(/&amp;/gi,'&').replace(/&#39;/g,"'").replace(/&quot;/gi,'"').replace(/\s+/g,' ').trim();}
function any(t,arr){const h=String(t||'').toLowerCase();return arr.some(x=>h.includes(x));}
function ageDays(v){const t=new Date(v).getTime();return Number.isFinite(t)?Math.max(0,(Date.now()-t)/86400000):Infinity;}
function locationFits(v){const s=plain(v).toLowerCase();return !s||LOC.some(x=>s.includes(x));}
function score(j){
  const title=plain(j.title).toLowerCase();
  const body=`${title} ${plain(j.description).toLowerCase()} ${plain(j.tags).toLowerCase()}`;
  let n=0;
  if(any(title,STRONG)) n+=5; else if(any(body,STRONG)) n+=3;
  if(any(body,SUPPORT)) n+=2;
  if(any(body,CONTRACT)||any(j.jobType,CONTRACT)) n+=2;
  n+=locationFits(j.location)?1:-3;
  if(any(body,TECH)) n+=1;
  if(any(title,SENIOR)) n-=2;
  if(String(j.jobType||'').toLowerCase()==='full_time') n-=1;
  return n;
}
async function getJson(url){
  const r=await fetch(url,{headers:{Accept:'application/json','User-Agent':'AI-Media-Video-Lead-Worker/1.0'},signal:AbortSignal.timeout(20000)});
  if(!r.ok) throw new Error(`HTTP ${r.status} from ${url}`);
  return r.json();
}
async function sources(){
  const rs=await Promise.allSettled([
    getJson('https://remotive.com/api/remote-jobs?search=video%20editor&limit=100'),
    getJson('https://remoteok.com/api')
  ]);
  const jobs=[], errors=[];
  if(rs[0].status==='fulfilled'){
    for(const j of rs[0].value.jobs||[]) jobs.push({source:'Remotive',id:String(j.id),title:j.title,company:j.company_name,date:j.publication_date,location:j.candidate_required_location,jobType:j.job_type,salary:j.salary||'',description:plain(j.description),tags:j.category||'',url:j.url});
  } else errors.push(String(rs[0].reason?.message||rs[0].reason));
  if(rs[1].status==='fulfilled'){
    const rows=Array.isArray(rs[1].value)?rs[1].value.slice(1):[];
    for(const j of rows) jobs.push({source:'Remote OK',id:String(j.id||j.slug||j.url),title:j.position,company:j.company,date:j.date||(j.epoch?new Date(Number(j.epoch)*1000).toISOString():''),location:j.location,jobType:(j.tags||[]).join(' '),salary:(j.salary_min||j.salary_max)?`${j.salary_min||''}-${j.salary_max||''}`:'',description:plain(j.description),tags:(j.tags||[]).join(' '),url:j.apply_url||j.url});
  } else errors.push(String(rs[1].reason?.message||rs[1].reason));
  if(!jobs.length && errors.length) throw new Error(errors.join(' | '));
  return {jobs,errors};
}
async function waSend(to,payload){
  const token=process.env.WHATSAPP_TOKEN, phone=process.env.WHATSAPP_PHONE_NUMBER_ID;
  if(!token||!phone) return {ok:false,status:'blocked',error:'WhatsApp env missing'};
  const r=await fetch(`https://graph.facebook.com/${process.env.GRAPH_API_VERSION||'v23.0'}/${phone}/messages`,{
    method:'POST',headers:{Authorization:`Bearer ${token}`,'Content-Type':'application/json'},
    body:JSON.stringify({messaging_product:'whatsapp',recipient_type:'individual',to,...payload}),
    signal:AbortSignal.timeout(15000)
  });
  const data=await r.json().catch(()=>({}));
  if(!r.ok) return {ok:false,status:'failed',error:data?.error?.message||`HTTP ${r.status}`,code:data?.error?.code};
  return {ok:true,status:'accepted',id:data.messages?.[0]?.id||null};
}
function compact(j){return `${j.company||'Unknown'} — ${j.title}${j.salary?' • '+plain(j.salary):''} — ${j.url}`;}

module.exports = async function handler(req,res){
  if(req.headers.authorization!==`Bearer ${process.env.CRON_SECRET}`) return res.status(401).json({ok:false,error:'unauthorized'});
  const uri=process.env.MONGODB_URI;
  if(!uri) return res.status(503).json({ok:false,error:'MONGODB_URI missing'});
  const client=new MongoClient(uri);
  let locked=false;
  try{
    await client.connect();
    const db=client.db();
    const statuses=db.collection('systemstatuses');
    const now=new Date();
    await statuses.updateOne({key:LOCK_KEY},{$setOnInsert:{key:LOCK_KEY,value:{lockUntil:new Date(0)},createdAt:now,updatedAt:now}},{upsert:true});
    const claim=await statuses.findOneAndUpdate({key:LOCK_KEY,'value.lockUntil':{$lte:now}},{$set:{'value.lockUntil':new Date(now.getTime()+LOCK_MS),'value.trigger':'vercel-worker',updatedAt:now}},{returnDocument:'after'});
    if(!claim) return res.status(200).json({ok:true,skipped:'locked'});
    locked=true;

    const state=(await statuses.findOne({key:STATE_KEY}))?.value||{};
    const seen=new Set(Array.isArray(state.seenIds)?state.seenIds:[]);
    const {jobs,errors}=await sources();
    const candidates=jobs.filter(j=>j.id&&j.url&&ageDays(j.date)<=MAX_AGE_DAYS).map(j=>({...j,score:score(j)})).filter(j=>j.score>=5).sort((a,b)=>b.score-a.score||new Date(b.date)-new Date(a.date));
    const fresh=[], runSeen=new Set();
    for(const j of candidates){const k=`${j.source}:${j.id}`;if(runSeen.has(k))continue;runSeen.add(k);if(!seen.has(k))fresh.push({...j,key:k});}
    const top=fresh.slice(0,5);
    if(!top.length){
      await statuses.updateOne({key:STATE_KEY},{$set:{value:{...state,checkedAt:now,sources:['Remotive','Remote OK'],lastNewCount:0,lastTop:[],sourceErrors:errors},updatedAt:now}},{upsert:true});
      return res.status(200).json({ok:true,fetched:jobs.length,matched:candidates.length,newMatches:0,alerted:0});
    }

    const business=await db.collection('businesses').findOne({singleton:'main'});
    const owner=String(business?.ownerWhatsApp||'').replace(/\D/g,'');
    if(!owner) return res.status(503).json({ok:false,error:'ownerWhatsApp not configured'});

    const lines=top.map((j,i)=>`${i+1}. ${compact(j)}\nFit: ${j.score}/10`).join('\n\n');
    const text=`🔔 ${top.length} new video-editing lead${top.length===1?'':'s'}\n\n${lines}\n\nSources: Remotive + Remote OK`;
    const convo=await db.collection('conversations').findOne({waId:owner});
    const last=convo?.lastInboundAt?new Date(convo.lastInboundAt):null;
    const windowOpen=last && Date.now()-last.getTime()<24*60*60*1000-5*60*1000;
    let sent;
    if(windowOpen){
      sent=await waSend(owner,{type:'text',text:{body:text.slice(0,4096),preview_url:true}});
    }else if(process.env.TEMPLATE_OWNER_ALERT){
      const reason=top.slice(0,3).map(compact).join(' | ').slice(0,950);
      sent=await waSend(owner,{type:'template',template:{name:process.env.TEMPLATE_OWNER_ALERT,language:{code:process.env.TEMPLATE_LANGUAGE||'en'},components:[{type:'body',parameters:[{type:'text',text:`${top.length} video-editing leads`},{type:'text',text:reason}]}]}});
    }else{
      sent={ok:false,status:'blocked',error:'Owner 24h window closed and TEMPLATE_OWNER_ALERT is not configured'};
    }

    if(sent.ok){
      for(const j of fresh) seen.add(j.key);
      await statuses.updateOne({key:STATE_KEY},{$set:{value:{seenIds:Array.from(seen).slice(-MAX_SEEN),checkedAt:now,sources:['Remotive','Remote OK'],lastNewCount:fresh.length,lastTop:top.map(j=>({source:j.source,sourceId:j.id,title:j.title,company:j.company,url:j.url,score:j.score})),sourceErrors:errors,lastAlertStatus:sent.status},updatedAt:now}},{upsert:true});
    }else{
      await statuses.updateOne({key:STATE_KEY},{$set:{'value.checkedAt':now,'value.lastAlertStatus':sent.status,'value.lastAlertError':sent.error,'value.sourceErrors':errors,updatedAt:now}},{upsert:true});
    }
    return res.status(sent.ok?200:502).json({ok:sent.ok,fetched:jobs.length,matched:candidates.length,newMatches:fresh.length,alerted:sent.ok?top.length:0,alertStatus:sent.status,alertError:sent.error||null,alertCode:sent.code||null});
  }catch(e){
    return res.status(500).json({ok:false,error:e.message});
  }finally{
    try{if(locked){const db=client.db();await db.collection('systemstatuses').updateOne({key:LOCK_KEY},{$set:{'value.lockUntil':new Date(0),updatedAt:new Date()}});}}catch{}
    await client.close().catch(()=>{});
  }
};
