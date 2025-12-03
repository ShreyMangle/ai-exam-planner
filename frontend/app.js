
async function gen(){
 let d={
  subjects: document.getElementById("subjects").value.split(","),
  exam_date: document.getElementById("date").value,
  hours_per_day: parseInt(document.getElementById("hours").value)
 };
 let r = await fetch("/generate_plan",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify(d)
 });
 let j = await r.json();
 document.getElementById("out").innerText = JSON.stringify(j,null,2);
}
