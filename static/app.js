async function updateTables() {
    const response = await fetch('/api/status?t=' + Date.now());
    const data = await response.json();

    let freeCount = 0;

    for (const [table, status] of Object.entries(data)) {
        const el = document.getElementById(table);

        el.className = 'table ' + status;

        if (status === 'free') {
            el.innerHTML = `<h3>${table}</h3><p>ว่าง</p>`;
            freeCount++;
        } else {
            el.innerHTML = `<h3>${table}</h3><p>มีคนนั่ง</p>`;
        }
    }

    document.getElementById('freeCount').innerText = freeCount;
}

// โหลดครั้งแรก
updateTables();

// สุ่มใหม่ทุก 3 วินาที
setInterval(updateTables, 3000);