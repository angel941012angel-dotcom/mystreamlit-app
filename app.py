import streamlit as st
import streamlit.components.v1 as components

st.title("📋 課程回饋表單")
st.write("請填寫以下資料，完成後按下送出。")

# 1. 姓名
name = st.text_input("姓名", placeholder="請輸入姓名")

# 2. 科系下拉選單（工程學院基本科系）
department = st.selectbox(
    "科系",
    [
        "請選擇科系",
        "資訊工程系",
        "電機工程系",
        "電子工程系",
        "機械工程系",
        "化學工程與材料工程系",
        "營建工程系",
        "環境與安全衛生工程系"
    ]
)

# 3. 滿意度與意見回饋
satisfaction = st.slider("課程滿意度", 1, 5, 3)
feedback = st.text_area("意見回饋", placeholder="請輸入您的意見回饋...")

# 檢查各欄位填寫狀況
missing_fields = []
if not name.strip():
    missing_fields.append("姓名尚未填寫")
if department == "請選擇科系":
    missing_fields.append("尚未選擇科系")
if not feedback.strip():
    missing_fields.append("意見回饋尚未填寫")

is_completed = len(missing_fields) == 0

# 4. 未完成資料提示指標
if not is_completed:
    st.info(f"📌 **尚未完成的項目（共 {len(missing_fields)} 項）：**\n- " + "\n- ".join(missing_fields))
else:
    st.success("✅ 資料已完整填寫，按鈕已解鎖並回歸原位！")

# 5. 前端 JavaScript 邏輯：未完成時逃跑；完成時重置回原位
if not is_completed:
    components.html(
        """
        <script>
        const parentDoc = window.parent.document;
        let isMoving = false;

        function attachRunawayBehavior() {
            const buttons = Array.from(parentDoc.querySelectorAll('button'));
            const btn = buttons.find(b => b.innerText.includes("送出"));

            if (!btn || btn.dataset.runawayAttached === "active") return;
            btn.dataset.runawayAttached = "active";

            btn.style.transition = "transform 0.15s ease-out";
            btn.style.willChange = "transform";

            const onMouseMove = (e) => {
                if (btn.dataset.runawayAttached !== "active") return;

                const rect = btn.getBoundingClientRect();
                const btnCenterX = rect.left + rect.width / 2;
                const btnCenterY = rect.top + rect.height / 2;

                const distX = e.clientX - btnCenterX;
                const distY = e.clientY - btnCenterY;
                const distance = Math.hypot(distX, distY);

                // 游標逼近小於 100px 時逃跑
                if (distance < 100 && !isMoving) {
                    isMoving = true;
                    const angle = Math.atan2(distY, distX) + (Math.random() - 0.5);
                    const escapeDist = 120 + Math.random() * 80;

                    const moveX = -Math.cos(angle) * escapeDist;
                    const moveY = -Math.sin(angle) * escapeDist;

                    btn.style.transform = `translate(${moveX}px, ${moveY}px)`;

                    setTimeout(() => {
                        isMoving = false;
                    }, 120);
                }
            };

            parentDoc.removeEventListener('mousemove', parentDoc._runawayHandler);
            parentDoc._runawayHandler = onMouseMove;
            parentDoc.addEventListener('mousemove', onMouseMove);
        }

        const interval = setInterval(attachRunawayBehavior, 200);
        setTimeout(() => clearInterval(interval), 4000);
        </script>
        """,
        height=0,
        width=0,
    )
else:
    # 資料已齊全：移除逃跑事件並強制將按鈕位置 reset 回 (0, 0)
    components.html(
        """
        <script>
        const parentDoc = window.parent.document;
        const buttons = Array.from(parentDoc.querySelectorAll('button'));
        const btn = buttons.find(b => b.innerText.includes("送出"));

        if (btn) {
            btn.dataset.runawayAttached = "disabled";
            btn.style.transition = "transform 0.3s ease-out";
            btn.style.transform = "translate(0px, 0px)";
        }

        if (parentDoc._runawayHandler) {
            parentDoc.removeEventListener('mousemove', parentDoc._runawayHandler);
        }
        </script>
        """,
        height=0,
        width=0,
    )

# 6. 送出按鈕與顯示結果
if st.button("送出"):
    st.balloons()
    st.success("🎉 成功上傳！感謝您的回饋。")
    st.write("**姓名：**", name)
    st.write("**科系：**", department)
    st.write("**課程滿意度：**", satisfaction, "分")
    st.write("**意見回饋：**", feedback)