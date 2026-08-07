async function updateTables() {
    try {
        // ดึงข้อมูลล่าสุดจาก Flask
        const response = await fetch('/api/status?t=' + new Date().getTime());
        const data = await response.json();

        let freeCount = 0;

        for (const [table, status] of Object.entries(data)) {
            const el = document.getElementById(table);

            if (!el) continue;

            // เปลี่ยนสีของกล่อง
            el.className = 'table ' + status;

            // เปลี่ยนข้อความ
            if (status === 'free') {
                el.innerHTML = `<h3>${table}</h3><p>ว่าง</p>`;
                freeCount++;
            } else {
                el.innerHTML = `<h3>${table}</h3><p>มีคนนั่ง</p>`;
            }
        }

        // อัปเดตจำนวนโต๊ะว่าง
        document.getElementById('freeCount').innerText = freeCount;

    } catch (error) {
        console.log('โหลดข้อมูลไม่สำเร็จ', error);
    }
}

// โหลดทันทีเมื่อเปิดเว็บ
updateTables();

// อัปเดตทุก 1 วินาที
setInterval(updateTables, 1000);