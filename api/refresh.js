// Vercel 后端中转站函数
export default async function handler(req, res) {
  // 只允许 POST 请求（网页端发送过来的信号）
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  // 1. 从刚才的保险箱里取出隐藏的钥匙
  const token = process.env.MY_GITHUB_TOKEN;
  
  // 【配置区】换成你自己的 GitHub 用户名和仓库名
  const owner = "xsorainfo"; 
  const repo = "my-stock-web"; 

  if (!token) {
    return res.status(500).json({ error: 'Vercel 后台未配置 MY_GITHUB_TOKEN' });
  }

  try {
    // 2. 由 Vercel 后台服务器替你去呼叫 GitHub 机器人
    const url = `https://api.github.com/repos/${owner}/${repo}/dispatches`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": `token ${token}`
      },
      body: JSON.stringify({ event_type: "web_refresh" })
    });

    if (response.status === 204) {
      return res.status(200).json({ success: true });
    } else {
      const errText = await response.text();
      return res.status(response.status).json({ error: errText });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
