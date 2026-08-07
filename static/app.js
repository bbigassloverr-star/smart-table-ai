async function updateTables() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        let freeCount = 0;

        for (const [table, status] of Object.entries(data)) {
            const el = document.getElementById(table);

            if (!el) continue;

            el.className = 'table ' + status;

            if (status === 'free') {
                el.innerHTML = `<h2>${table}</h2><p>ว่าง</p>`;
                freeCount++;
            } else {
                el.innerHTML = `<h2>${table}</h2><p>มีคนนั่ง</p>`;
            }
        }

        document.getElementById('freeCount').innerText = freeCount;

    } catch (err) {
        console.error('โหลดข้อมูลไม่สำเร็จ', err);
    }
}

updateTables();
setInterval(updateTables, 1000);