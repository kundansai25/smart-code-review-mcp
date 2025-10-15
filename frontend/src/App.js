import React, {useState} from 'react';

function App(){
  const [repo, setRepo] = useState('');
  const [resp, setResp] = useState(null);

  const submit = async () => {
    const r = await fetch('/mcp/review', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({repo_url: repo})
    });
    const j = await r.json();
    setResp(j);
  };

  return (<div style={{padding:20}}>
    <h1>Smart Code Review MCP — Demo</h1>
    <input style={{width:'80%'}} placeholder="https://github.com/owner/repo" value={repo} onChange={e=>setRepo(e.target.value)} />
    <button onClick={submit}>Request Review</button>
    <pre>{JSON.stringify(resp, null, 2)}</pre>
  </div>);
}

export default App;
