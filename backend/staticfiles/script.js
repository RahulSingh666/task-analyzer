const apiBase = '/api/tasks';

let localTasks = [];

function renderTasks(list){
  const el = document.getElementById('results');
  el.innerHTML = '';
  list.forEach(t => {
    const div = document.createElement('div');
    let cls = 'task low';
    if(t.score >= 0.75) cls = 'task high';
    else if(t.score >= 0.45) cls = 'task medium';
    div.className = cls;
    div.innerHTML = `<strong>${t.title}</strong> <span class="meta">score: ${t.score}</span>
      <div class="meta">due: ${t.due_date || '—'} | est: ${t.estimated_hours}h | importance: ${t.importance}</div>
      <div class="explain">${t.explanation}</div>`;
    el.appendChild(div);
  });
}

document.getElementById('taskForm').addEventListener('submit', e=>{
  e.preventDefault();
  const t = {
    id: 'id_' + Math.random().toString(36).slice(2,8),
    title: document.getElementById('t_title').value,
    due_date: document.getElementById('t_due').value || null,
    estimated_hours: parseFloat(document.getElementById('t_est').value) || 1.0,
    importance: parseInt(document.getElementById('t_imp').value) || 5,
    dependencies: document.getElementById('t_deps').value.split(',').map(s=>s.trim()).filter(Boolean)
  };
  localTasks.push(t);
  alert('Task added locally. Click Analyze to score.');
  document.getElementById('taskForm').reset();
});

document.getElementById('analyzeBtn').addEventListener('click', async ()=>{
  const bulk = document.getElementById('bulk').value.trim();
  let tasks = localTasks.slice();
  if(bulk){
    try{
      const parsed = JSON.parse(bulk);
      if(Array.isArray(parsed)) tasks = parsed;
      else alert('Bulk JSON must be an array');
    }catch(err){
      alert('Invalid JSON in bulk input');
      return;
    }
  }
  if(tasks.length === 0){
    alert('No tasks to analyze. Add a task or paste JSON.');
    return;
  }
  const strategy = document.getElementById('strategy').value;
  const body = { tasks, options: { strategy } };
  try{
    const res = await fetch(apiBase + '/analyze/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if(!res.ok){
      const txt = await res.text(); throw new Error(txt);
    }
    const data = await res.json();
    renderTasks(data.results);
  }catch(err){
    alert('Error: ' + err.message);
  }
});

document.getElementById('suggestBtn').addEventListener('click', async ()=>{
  const bulk = document.getElementById('bulk').value.trim();
  let tasks = localTasks.slice();
  if(bulk){
    try{ const parsed = JSON.parse(bulk); if(Array.isArray(parsed)) tasks = parsed; }catch(err){ alert('Invalid JSON'); return; }
  }
  const strategy = document.getElementById('strategy').value;
  let url = apiBase + '/suggest/?strategy=' + encodeURIComponent(strategy);
  if(tasks.length) url += '&tasks=' + encodeURIComponent(JSON.stringify(tasks));
  try{
    const res = await fetch(url);
    if(!res.ok){ throw new Error(await res.text()); }
    const data = await res.json();
    renderTasks(data.suggestions.map(s=>({title:s.title, score:s.score, due_date:null, estimated_hours:'—', importance:'—', explanation:s.why})));
  }catch(err){
    alert('Error: ' + err.message);
  }
});
