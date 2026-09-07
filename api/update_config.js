export default async function handler(req, res) {
  const password = process.env.CONFIG_EDIT_PASSWORD;
  if (!password) return res.status(503).json({error:'请先配置 CONFIG_EDIT_PASSWORD'});
  if (req.headers.authorization !== \`Bearer \${password}\`) return res.status(401).json({error:'密码错误'});
  const files = {watchlist:'config.py',sector_mapping:'data/sector_mapping.json',tag_display_map:'scripts/tag_display_map.py',theme_mapping:'scripts/theme_mapping.py',portfolio_lists:'scripts/portfolio_lists.py'};
  const key = req.query?.key || req.body?.key;
  if (!files[key]) return res.status(400).json({error:'未知配置'});
  const owner=process.env.GITHUB_REPO_OWNER||'xsorainfo', repo=process.env.GITHUB_REPO_NAME||'my-stock-web', token=process.env.GITHUB_TOKEN||process.env.MY_REPO_TOKEN;
  if (!token) return res.status(503).json({error:'GitHub 写入凭据未配置'});
  const path=files[key];
  try {
    const current=await gh(owner,repo,'contents/'+path,token);
    if(req.method==='GET') return res.status(200).json({key,content:Buffer.from(current.content,'base64').toString('utf8')});
    if(req.method!=='PUT') return res.status(405).json({error:'只支持 GET 或 PUT'});
    const content=req.body?.content;
    if(typeof content!=='string'||content.length>1000000) return res.status(400).json({error:'内容无效或过大'});
    if(!content.includes(key==='watchlist'?'WATCHLIST':key==='sector_mapping'?'[':key.toUpperCase())) return res.status(400).json({error:'内容缺少必要结构'});
    await gh(owner,repo,'contents/'+path,token,'PUT',{message:'Update '+key+' from config editor',content:Buffer.from(content).toString('base64'),sha:current.sha});
    return res.status(200).json({success:true});
  } catch(e){return res.status(e.status===409?409:500).json({error:e.message});}
}
async function gh(owner,repo,path,token,method='GET',body){const r=await fetch(\`https://api.github.com/repos/\${owner}/\${repo}/\${path}\`,{method,headers:{Accept:'application/vnd.github+json',Authorization:'Bearer '+token,'Content-Type':'application/json'},...(body?{body:JSON.stringify(body)}:{})});if(!r.ok){const e=new Error('GitHub request failed ('+r.status+')');e.status=r.status;throw e;}return r.status===204?null:r.json();}