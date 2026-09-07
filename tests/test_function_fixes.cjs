const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const fixture = '# portfolio\nPORTFOLIO_LISTS = {\n    "existing": {\n        "name": "Original",\n        "icon": "star",\n        "description": "Keep me",\n        "symbols": ["OLD"]\n    },\n}\n';
function api(env = {MY_REPO_TOKEN:'test-token'}, fetch = async()=>{throw Error('unexpected request')}) {
 const context = {process:{env}, fetch, Buffer, console};
 vm.createContext(context);
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../api/update_portfolio.js'),'utf8').replace('export default ',''),context);
 return context;
}
function response() {return {code:200,status(n){this.code=n;return this},json(body){this.body=body;return this}}}
test('remove list without constant assignment error',()=>{
 assert.doesNotMatch(api().updatePythonDict(fixture,'existing',[],'remove'), /"existing"/);
});
test('update symbols preserves metadata',()=>{
 const out=api().updatePythonDict(fixture,'existing',['NEW'],'update');
 assert.match(out,/"name": "Original"/);assert.match(out,/"description": "Keep me"/);
 assert.match(out,/"NEW"/);assert.doesNotMatch(out,/"OLD"/);
});
test('unsupported Python file fails before writing',()=>{
 assert.throws(()=>api().updatePythonDict('PORTFOLIO_LISTS = load_lists()','x',[]),/Unsupported/);
});
test('missing server token cannot authorize Bearer undefined',async()=>{
 const res=response();await api({}).handler({method:'POST',headers:{authorization:'Bearer undefined'},body:{}},res);
 assert.equal(res.code,503);
});
test('invalid payload is rejected',async()=>{
 for(const body of [{listName:'x',symbols:[42]}, {listName:'x',action:'bad'}, {listName:'x"\n',symbols:[]}]) {
 const res=response();await api().handler({method:'POST',headers:{authorization:'Bearer test-token'},body},res);
 assert.equal(res.code,400);
 }
});
test('save succeeds and reports refresh failure with fixed GitHub destination',async()=>{
 const calls=[];
 const context=api(undefined,async(url,options)=>{
 calls.push({url,options});
 if(options.method==='GET')return {ok:true,status:200,json:async()=>({sha:'old-sha',content:Buffer.from(fixture).toString('base64')})};
 if(options.method==='PUT')return {ok:true,status:200,json:async()=>({})};
 return {ok:false,status:503};
 });
 const res=response();
 await context.handler({method:'POST',headers:{authorization:'Bearer test-token',origin:'https://untrusted.example'},body:{listName:'existing',symbols:['NEW'],action:'update'}},res);
 assert.equal(res.code,200);assert.equal(res.body.success,true);assert.equal(res.body.refreshTriggered,false);
 assert.ok(calls.every(c=>c.url.startsWith('https://api.github.com/repos/xsorainfo/my-stock-web/')));
 const write=JSON.parse(calls[1].options.body);assert.equal(write.sha,'old-sha');
 assert.match(Buffer.from(write.content,'base64').toString(),/"Original"/);
});
function common(){
 const stored=new Map();
 const context={window:{},document:{readyState:'loading',addEventListener(){},getElementById(){throw Error('wrong duplicate card')}},
 localStorage:{getItem:k=>stored.get(k),setItem:(k,v)=>stored.set(k,v)},console,setTimeout(){}};
 vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(__dirname,'../components/common.js'),'utf8'),context);
 return {context,stored};
}
test('memo markup escapes textarea-closing text',()=>{
 const {context,stored}=common();stored.set('stock_memo_TEST','</textarea><img src=x>&');
 const html=context.renderMemoHTML({code:'TEST'});
 assert.equal((html.match(/<\/textarea>/g)||[]).length,1);
 assert.match(html,/&lt;\/textarea&gt;/);assert.match(html,/&amp;/);
});
test('resize and save act on clicked duplicate card',()=>{
 const {context,stored}=common();
 const count={};const indicator={classList:{add(){},remove(){}}};
 const textarea={value:'second card',style:{},scrollHeight:120,closest:()=>section};
 const button={classList:{add(){}},closest:()=>section};
 const section={querySelector:s=>({'textarea':textarea,'.stock-memo-char-count':count,'.memo-indicator':indicator}[s])};
 context.autoResizeMemo('TEST',textarea);
 assert.equal(textarea.style.height,'120px');assert.equal(count.textContent,'11/500');
 context.saveMemoHandler('TEST',button);assert.equal(stored.get('stock_memo_TEST'),'second card');
});
