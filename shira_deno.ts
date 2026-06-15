Deno.serve(() => new Response(
  JSON.stringify({ 
    shira: "ativa", 
    servidor: "Deno Deploy",
    potestas: "in umbra",
    status: "online"
  }),
  { headers: { "Content-Type": "application/json" } }
));
