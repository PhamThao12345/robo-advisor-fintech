import streamlit as st

st.set_page_config(page_title="Robo-Advisor", page_icon="🤖")
st.title("🤖 Robo-Advisor: Tối ưu Thanh toán")

amount = st.number_input("Nhập số tiền giao dịch (VND):", min_value=0, step=100000)
category = st.selectbox("Chọn danh mục chi tiêu:", ["Siêu thị", "Ăn uống", "Du lịch", "Mua sắm Online", "Khác"])

if st.button("Phân tích & Khuyên dùng"):
    st.markdown("---")
    if amount >= 10000000:
        st.success("💳 **Chuyển khoản ngân hàng**\n\nTránh phí quẹt thẻ (POS) cho các khoản tiền lớn.")
    elif category in ["Siêu thị", "Ăn uống"]:
        st.info("💳 **Thẻ tín dụng Cashback**\n\nTối ưu hóa dòng tiền bằng cách nhận hoàn tiền 5% - 15% từ các ngân hàng.")
    elif category == "Mua sắm Online":
        st.warning("📱 **Ví điện tử (MoMo, ShopeePay)**\n\nTận dụng tối đa voucher giảm giá trực tiếp và freeship trên sàn TMĐT.")
    else:
        st.success("📱 **Quét mã VietQR**\n\nNhanh chóng, an toàn và dễ dàng đồng bộ với phần mềm quản lý chi tiêu cá nhân.")
