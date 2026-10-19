import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & GIAO DIỆN HALLOWEEN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tiệm Trà Lời Nguyền - Halloween Edition",
    page_icon="🎃",
    layout="wide"
)

# Custom CSS giao diện u tối, ma mị
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: #e0e0e0;
    }
    h1, h2, h3 {
        color: #ff6600 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #660099 !important;
        color: white !important;
        border: 1px solid #ff6600 !important;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #ff6600 !important;
        color: black !important;
        border: 1px solid #660099 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Đổi ảnh banner hoặc hiển thị tiêu đề rùng rợn
st.title("🎃 TIỆM TRÀ LỜI NGUYỀN (CURSED BUBBLE TEA)")
st.subheader("👻 Vị Ngon Độc Huyết - Uống Là Mất Hồn 🩸")

# ---------------------------------------------------------
# 2. CƠ SỞ DỮ LIỆU MENUS & TÙY CHỌN HALLOWEEN
# ---------------------------------------------------------
# Menu nước uống kinh dị
MENU_TEA = {
    "🩸 Máu Ma Cà Rồng (Trà Dâu Tằm Kem Béo Red Velvet)": 45000,
    "🧪 Nước Cất Phù Thủy (Lục Trà Táo Xanh & Bạc Hà Mắt Quỷ)": 42000,
    "🕷️ Độc Tố Nhện Đen (Trà Sữa Sô-cô-la Đen Than Hoạt Tính)": 48000,
    "🧠 Não Người Chiên Xù (Matcha Latte Đậu Đỏ Dầm)": 46000,
    "🎃 Linh Hồn Bí Ngô (Trà Sữa Bí Ngô Kem Cháy Spiced Pumpkin)": 49000,
    "👁️ Lòng Con Ngươi (Trà Trái Cây Đột Biến Topping Thạch Mắt)": 44000,
    "🦴 Súp Xương Tử Thần (Trà Oolong Sữa Than Tre & Khúc Bạch)": 47000,
}

SIZE_OPTIONS = {
    "Linh Hồn Tí Hon (S - Thử Tẩy Băng)": 0,
    "Trại Hòm Trung Bình (M - Vừa Đủ Rùng Rợn)": 8000,
    "Quan Tài Khổng Lồ (L - Nuốt Chửng Đêm Đen)": 15000
}

TOPPING_OPTIONS = {
    "👁️ Thạch Con Ngươi Giòn Sần Sật": 8000,
    "🧠 Brain-Pudding (Pudding Não Trứng Béo)": 9000,
    "🐛 Sâu Bọ Trân Châu Đen Dẻo Quánh": 7000,
    "🩸 Sốt Máu Rồng (Rô-ti Dâu Tây Đỏ)": 8000,
    "🦴 Vụn Xương Đầu Nhai Rạo Rực (Dừa Nướng Cháy)": 10000,
    "👻 Kem Mây Ma Hồn (Kem Cheese Béo Ngậy)": 12000
}

SUGAR_LEVELS = [
    "100% Độc Đậm Đà (Ngọt Ngào Chết Người)",
    "70% Độc Nhẹ (Tê Lưỡi)",
    "50% Độc Trung Bình (Tỉnh Giấc Đêm Thanh)",
    "30% Độc Thoang Thoảng (Yếu Ớt)",
    "0% Thuần Khiết (Không Đường - Như Trống Rỗng)"
]

ICE_LEVELS = [
    "100% Băng Giá Âm Phủ (Lạnh Tắt Hơi Hở)",
    "70% Sương Lạnh Đêm Âm",
    "50% Gió Lạnh Buốt Cốt",
    "30% Hơi Ấm Nghĩa Địa",
    "0% Thiêu Đốt Giữa Hỏa Ngục (Không Đá)"
]

# Khởi tạo Session State
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False

# ---------------------------------------------------------
# 3. HÀM TẠO HÓA ĐƠN VĂN BẢN (TXT)
# ---------------------------------------------------------
def create_txt_invoice(customer_name, cart, total_amount, discount, final_amount):
    """Tạo file hóa đơn dạng văn bản (TXT) đậm chất Halloween"""
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    content = f"{'='*45}\n"
    content += f"{'🎃 TIỆM TRÀ LỜI NGUYỀN - BILL BÁN HỒN 🎃':^45}\n"
    content += f"{'='*45}\n"
    content += f"Thời gian hiến tế: {now}\n"
    content += f"Linh hồn nhận trà: {customer_name if customer_name else 'Kẻ Vô Danh'}\n"
    content += f"{'-'*45}\n"
    
    for idx, item in enumerate(cart, 1):
        content += f"{idx}. {item['Tên món']} [{item['Size']}]\n"
        content += f"   - Độc tố đường: {item['Đường']} | Băng giá: {item['Đá']}\n"
        if item['Topping'] != "Không":
            content += f"   - Dị vật kềm theo: {item['Topping']}\n"
        content += f"   SL: {item['Số lượng']} x {item['Đơn giá']:,} = {item['Thành tiền']:,} VNĐ\n"
        
    content += f"{'-'*45}\n"
    content += f"Tổng phí linh hồn: {total_amount:,} VNĐ\n"
    content += f"Chiết khấu bùa phép: {discount}%\n"
    content += f"TỔNG GIÁ TRỊ TẾ LỄ: {final_amount:,} VNĐ\n"
    content += f"{'='*45}\n"
    content += f"{'Hẹn gặp lại ở Cõi Âm! Mwahahaha! 🧛‍♂️':^45}\n"
    return content

# ---------------------------------------------------------
# 4. GIAO DIỆN CHÍNH (LAYOUT 2 CỘT)
# ---------------------------------------------------------
col_left, col_right = st.columns([1.1, 0.9])

# ==================== CỘT TRÁI: ĐẶT TRÀ & BÓI AI ====================
with col_left:
    st.subheader("📜 Tờ Chế Bùa (Nhập Đơn Hàng)")
    
    # 1. Tên linh hồn
    customer_name = st.text_input("💀 Tên linh hồn đặt nước:", placeholder="Nhập tên người chịu lời nguyền...")
    
    st.markdown("#### 🧪 Chọn Thuốc Độc & Dị Vật")
    
    # 2. Chọn món & số lượng
    col_item, col_qty = st.columns([3, 1])
    with col_item:
        selected_tea = st.selectbox("🔮 Độc chất chính:", list(MENU_TEA.keys()))
    with col_qty:
        quantity = st.number_input("Liều lượng:", min_value=1, value=1, step=1)

    # 3. Size, Đường, Đá
    c_size, c_sugar, c_ice = st.columns(3)
    with c_size:
        selected_size = st.selectbox("⚰️ Loại Quan Tài (Size):", list(SIZE_OPTIONS.keys()))
    with c_sugar:
        selected_sugar = st.selectbox("🩸 Mức Độc Đường:", SUGAR_LEVELS)
    with c_ice:
        selected_ice = st.selectbox("❄️ Mức Đá Âm Phủ:", ICE_LEVELS)

    # 4. Topping
    selected_toppings = st.multiselect(
        "🕷️ Dị vật đi kèm (Topping):",
        options=list(TOPPING_OPTIONS.keys())
    )

    # --- TRỢ LÝ AI: BÓI TRÀ SỮA THEO TÂM TRẠNG MA QUỶ ---
    st.markdown("---")
    st.subheader("🔮 Cầu Cơ AI: Bói Trà Lời Nguyền")
    mood = st.selectbox(
        "Đêm nay, nỗi sợ nào đang ám ảnh bạn?", 
        [
            "🩸 Thèm máu & sự rùng rợn", 
            "💻 Bị deadline ám gục ngã", 
            "🖤 Tội lỗi & Trống rỗng", 
            "🔥 Cuồng sát, cần xả stress"
        ]
    )

    if st.button("🔮 Phán Truyền Bùa Phép"):
        if "Thèm máu" in mood:
            ai_pick = "🩸 Máu Ma Cà Rồng (Trà Dâu Tằm Kem Béo Red Velvet)"
            comment = "Vị chua ngọt đậm đà sẽ đánh thức bản năng quỷ dữ trong bạn!"
        elif "deadline" in mood:
            ai_pick = "🧪 Nước Cất Phù Thủy (Lục Trà Táo Xanh & Bạc Hà Mắt Quỷ)"
            comment = "Bạc hà buốt óc cùng độc tố táo xanh sẽ ép bạn thức đến 4h sáng!"
        elif "Trống rỗng" in mood:
            ai_pick = "🕷️ Độc Tố Nhện Đen (Trà Sữa Sô-cô-la Đen Than Hoạt Tính)"
            comment = "Vị đắng nhẹ quyện béo ngậy sẽ lấp đầy khoảng trống linh hồn."
        else:
            ai_pick = "🎃 Linh Hồn Bí Ngô (Trà Sữa Bí Ngô Kem Cháy Spiced Pumpkin)"
            comment = "Sức mạnh bão lửa từ bí ngô nướng sẽ thiêu rụi mọi mệt mỏi!"
        
        st.error(f"🧙‍♀️ **Phù Thủy AI Truyền Rằng:** Bạn nên uống **{ai_pick}**\n\n_{comment}_")

    # Tính giá tiền
    base_price = MENU_TEA[selected_tea]
    size_price = SIZE_OPTIONS[selected_size]
    topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity

    st.info(f"🪙 Phí tổn 1 ly độc tố: **{unit_price:,} VNĐ**")

    # Thêm vào giỏ
    if st.button("➕ Dâng Lên Món Này", type="primary", use_container_width=True):
        topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
        item_data = {
            "Tên món": selected_tea,
            "Size": selected_size.split()[0], 
            "Đường": selected_sugar.split()[0],
            "Đá": selected_ice.split()[0],
            "Topping": topping_str,
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        }
        st.session_state.cart.append(item_data)
        st.session_state.invoice_paid = False
        st.toast(f"Đã nạp **{quantity}x {selected_tea}** vào vạc dầu!", icon="🕷️")

# ==================== CỘT PHẢI: VẠC DẦU (GIỎ HÀNG) ====================
with col_right:
    st.subheader("🧺 Vạc Dầu Hiến Tế (Giỏ Hàng)")

    if not st.session_state.cart:
        st.warning("⚠️ Vạc dầu đang trống rỗng... Hãy dâng tế món uống bên trái.")
    else:
        df_cart = pd.DataFrame(st.session_state.cart)
        
        # Bảng hiển thị
        st.dataframe(
            df_cart[["Tên món", "Size", "Topping", "Số lượng", "Đơn giá", "Thành tiền"]],
            use_container_width=True,
            hide_index=True
        )

        # Xóa giỏ hàng
        if st.button("🧹 Hủy Lời Nguyền (Xóa Hết)"):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()

        st.markdown("---")
        
        total_price = df_cart["Thành tiền"].sum()
        
        col_disc, col_pay = st.columns(2)
        with col_disc:
            discount = st.number_input("Bùa Giảm Giá (%):", min_value=0, max_value=100, value=0, step=5)
        
        final_price = int(total_price * (1 - discount / 100))

        st.markdown(f"### Tổng linh hồn: **{total_price:,} VNĐ**")
        if discount > 0:
            st.markdown(f"### Sau khi yểm bùa (-{discount}%): <span style='color:#ff0000'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

        # Nút xác nhận thanh toán
        if st.button("🩸 KÝ HỢP ĐỒNG MÁU (THANH TOÁN)", type="primary", use_container_width=True):
            st.session_state.invoice_paid = True
            st.snow() # Tạo hiệu ứng tuyết/sương lạnh

# ---------------------------------------------------------
# 5. XUẤT HÓA ĐƠN ÂM PHỦ KHI THANH TOÁN
# ---------------------------------------------------------
if st.session_state.get("invoice_paid") and st.session_state.cart:
    st.markdown("---")
    st.error("🎉 HỢP ĐỒNG ĐÃ ĐƯỢC KÝ BẰNG MÁU! Dưới đây là tờ giấy bán hồn:")

    invoice_box = st.container(border=True)
    with invoice_box:
        st.markdown("<h2 style='text-align: center; color: #ff6600;'>🎃 HÓA ĐƠN BÁN HỒN - CURSED TEA 🎃</h2>", unsafe_allow_html=True)
        st.write(f"**Thời gian hiến tế:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        st.write(f"**Linh hồn sở hữu:** {customer_name if customer_name else 'Kẻ Vô Danh'}")
        
        st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Đường", "Đá", "Topping", "Số lượng", "Thành tiền"]])
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Tổng tổn thất:** {total_price:,} VNĐ")
            st.write(f"**Chiết khấu yểm bùa:** {discount}%")
        with c2:
            st.markdown(f"### TỔNG GIÁ TRỊ TẾ LỄ: <span style='color:#ff0000'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)

    txt_data = create_txt_invoice(customer_name, st.session_state.cart, total_price, discount, final_price)
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Tải Tờ Giấy Bán Hồn (.TXT)",
            data=txt_data,
            file_name=f"HoaDon_Halloween_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl2:
        if st.button("🔄 Triệu Hồi Đơn Hàng Mới", use_container_width=True):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()
