from pathlib import Path
import streamlit as st
from db import (
    auth_user, get_products, get_suppliers, get_names,
    add_product, update_product, delete_product, in_orders
)

st.set_page_config(page_title="Каталог товаров", page_icon="📚", layout="wide")


st.markdown("""
<style>
.card {
    border: 1px solid #394150;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 16px;
    background: #111827;
}
.card-green { background: #0f3d2e; }
.card-blue { background: #102a43; }
.old-price { color: #ff4d4d; text-decoration: line-through; }
.new-price { color: white; font-size: 24px; font-weight: 800; }
.badge { padding: 5px 10px; border-radius: 10px; background: #064e3b; color: #bbf7d0; }
</style>
""", unsafe_allow_html=True)


def find_image(photo):
    if not photo:
        photo = "picture.png"

    paths = [
        Path(photo),
        Path("import") / photo,
        Path("import") / "picture.png",
    ]

    for path in paths:
        if path.exists():
            return str(path)
    return None


def login_page():
    st.title("Вход в систему")

    if Path("import/Icon.JPG").exists():
        st.image("import/Icon.JPG", width=120)

    login = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")

    col1, col2 = st.columns(2)

    if col1.button("Войти", type="primary"):
        user = auth_user(login, password)
        if user:
            st.session_state.user = user
            st.session_state.page = "products"
            st.rerun()
        else:
            st.error("Неверный логин или пароль")

    if col2.button("Войти как гость"):
        st.session_state.user = {"full_name": "Гость", "role": "Гость"}
        st.session_state.page = "products"
        st.rerun()


def product_form():
    user = st.session_state.user
    if user["role"] != "Администратор":
        st.error("Добавлять и изменять товары может только администратор")
        if st.button("Назад"):
            st.session_state.page = "products"
            st.rerun()
        return

    edit_article = st.session_state.get("edit_article")
    product = None

    if edit_article:
        products = get_products(search=edit_article)
        for item in products:
            if item["article"] == edit_article:
                product = item

    st.title("Редактирование товара" if product else "Добавление товара")

    with st.form("product_form"):
        article = st.text_input("Артикул", value=product["article"] if product else "", disabled=bool(product))
        name = st.text_input("Наименование", value=product["name"] if product else "")
        description = st.text_area("Описание", value=product["description"] if product else "")

        category = st.selectbox("Категория", get_names("categories") or ["Книги"])
        manufacturer = st.selectbox("Производитель", get_names("manufacturers") or ["Не указан"])
        supplier = st.selectbox("Поставщик", get_names("suppliers") or ["Не указан"])
        unit = st.selectbox("Единица измерения", get_names("units") or ["шт."])

        price = st.number_input("Цена", min_value=0.0, value=float(product["price"]) if product else 0.0)
        discount = st.number_input("Скидка", min_value=0, max_value=100, value=int(product["discount"]) if product else 0)
        stock = st.number_input("Количество на складе", min_value=0, value=int(product["stock_quantity"]) if product else 0)
        photo = st.text_input("Фото", value=product["photo_url"] if product else "picture.png")

        save = st.form_submit_button("Сохранить", type="primary")

    if save:
        if not article or not name:
            st.error("Артикул и наименование обязательны")
            return

        data = {
            "article": article,
            "name": name,
            "description": description,
            "category": category,
            "manufacturer": manufacturer,
            "supplier": supplier,
            "unit": unit,
            "price": price,
            "discount": discount,
            "stock_quantity": stock,
            "photo_url": photo,
        }

        if product:
            ok, msg = update_product(product["article"], data)
        else:
            ok, msg = add_product(data)

        if ok:
            st.success(msg)
            st.session_state.page = "products"
            st.rerun()
        else:
            st.error(msg)

    if st.button("Назад к товарам"):
        st.session_state.page = "products"
        st.rerun()


def products_page():
    user = st.session_state.user

    col1, col2 = st.columns([4, 1])
    col1.title("Каталог товаров")
    col2.write(user["full_name"])
    col2.write(user["role"])

    if col2.button("Выйти"):
        st.session_state.clear()
        st.rerun()

    search = ""
    supplier = "Все поставщики"
    sort = ""

    if user["role"] in ["Менеджер", "Администратор"]:
        st.subheader("Поиск, фильтр и сортировка")
        f1, f2, f3, f4 = st.columns([3, 2, 2, 1])
        search = f1.text_input("Поиск")
        supplier = f2.selectbox("Поставщик", ["Все поставщики"] + get_suppliers())
        sort = f3.selectbox("Сортировка по количеству", ["", "По возрастанию", "По убыванию"])

        if user["role"] == "Администратор":
            if f4.button("Добавить"):
                st.session_state.edit_article = None
                st.session_state.page = "form"
                st.rerun()

    products = get_products(search, supplier, sort)

    for p in products:
        card_class = "card"
        if int(p["stock_quantity"] or 0) == 0:
            card_class += " card-blue"
        elif int(p["discount"] or 0) > 15:
            card_class += " card-green"

        with st.container():
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns([1, 3, 2, 1])

            image = find_image(p["photo_url"])
            if image:
                c1.image(image, width=130)

            c2.subheader(f'{p["category"]} | {p["name"]}')
            c2.write(p["description"])
            c2.write(f'**Производитель:** {p["manufacturer"]}')
            c2.write(f'**Поставщик:** {p["supplier"]}')
            c2.markdown(f'<span class="badge">Артикул: {p["article"]}</span>', unsafe_allow_html=True)

            price = float(p["price"] or 0)
            discount = int(p["discount"] or 0)
            final_price = price * (1 - discount / 100)

            c3.write("**Цена:**")
            if discount > 0:
                c3.markdown(f'<div class="old-price">{price:.2f} ₽</div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="new-price">{final_price:.2f} ₽</div>', unsafe_allow_html=True)
            else:
                c3.markdown(f'<div class="new-price">{price:.2f} ₽</div>', unsafe_allow_html=True)

            c3.write(f'**Единица:** {p["unit"]}')
            c3.write(f'**На складе:** {p["stock_quantity"]}')
            c3.write(f'**Скидка:** {discount}%')

            if user["role"] == "Администратор":
                if c4.button("Изменить", key="edit_" + p["article"]):
                    st.session_state.edit_article = p["article"]
                    st.session_state.page = "form"
                    st.rerun()

                if c4.button("Удалить", key="delete_" + p["article"]):
                    ok, msg = delete_product(p["article"])
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            st.markdown('</div>', unsafe_allow_html=True)


def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "products":
        products_page()
    elif st.session_state.page == "form":
        product_form()


main()
