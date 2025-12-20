export default async function handler(req, res) {
  // Check if token exists (don't print the whole token for security!)
  const hasToken = !!process.env.GITHUB_TOKEN;
  const tokenPrefix = process.env.GITHUB_TOKEN ? process.env.GITHUB_TOKEN.substring(0, 4) : "NONE";

  try {
    const response = await fetch("https://api.github.com/user", {
      headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` }
    });
    const data = await response.json();
    
    res.status(200).json({
      tokenDetected: hasToken,
      tokenStart: tokenPrefix,
      githubStatus: response.status,
      githubUser: data.login || "Unauthorized"
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
export default function Page() {
  try {
    // Your existing logic here
    return (
       <div>Your UI</div>
    );
  } catch (error) {
    return <div style={{color: 'red'}}>Runtime Error: {error.message}</div>;
  }
}
