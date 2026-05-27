async function summarize() {
    let text = document.getElementById("text").value;

    let res = await fetch("/api/summarize?text=" + text);
    let data = await res.json();

    document.getElementById("out1").innerText = data.summary;
}

async function voice() {
    let text = document.getElementById("voiceText").value;

    let res = await fetch("/api/voice?text=" + text);
    let data = await res.json();

    document.getElementById("out2").innerText = "Voice generated: " + data.voice;
}
