from html import escape
from pathlib import Path

import streamlit as st

from controller import ParcelController
from i18n import translate, translate_error
from repository import StorageError


PAGES = ['home', 'register', 'collect', 'records', 'lockers']


def t(key, **values):
    return translate(key, st.session_state.get('language', 'zh'), **values)


def show_error(message):
    st.error(translate_error(message, st.session_state.get('language', 'zh')))


def clear_flow():
    for key in ('registration', 'verified_code', 'collected', 'pickup_code',
                'register_error', 'collect_error'):
        st.session_state.pop(key, None)


def navigate(page):
    clear_flow()
    st.session_state['page'] = page


def invalidate_code():
    for key in ('verified_code', 'collected', 'collect_error'):
        st.session_state.pop(key, None)


def home_button():
    st.button(t('back'), on_click=navigate, args=('home',), key='back_home')


def heading(text, centered=False):
    cls = ' class="center-title"' if centered else ''
    st.html(f'<h2{cls}>{escape(text)}</h2>')


# 独立输入控件及时保存草稿，切换语言时不会丢失已提交到会话的输入
# Standalone inputs save drafts promptly and preserve them when switching languages
def register_page(controller):
    heading(t('register'), True)
    with st.container(key='narrow_form'):
        name = st.text_input(t('name'), placeholder=t('name_hint'), max_chars=100, key='recipient_name')
        contact = st.text_input(t('contact'), placeholder=t('contact_hint'), max_chars=150, key='recipient_contact')
        tracking = st.text_input(t('tracking'), placeholder=t('tracking_hint'), max_chars=100, key='tracking_number')
        if st.button(t('register'), type='primary', key='submit_registration'):
            st.session_state.pop('registration', None)
            st.session_state.pop('register_error', None)
            try:
                st.session_state['registration'] = controller.register(name, contact, tracking).to_dict()
            except (ValueError, StorageError) as error:
                st.session_state['register_error'] = str(error)
        if message := st.session_state.get('register_error'):
            show_error(message)
    if result := st.session_state.get('registration'):
        st.divider()
        with st.container(key='registration_result'):
            st.subheader(t('registered'))
            st.write(t('assigned', number=result['locker_id']))
            st.write(t('code_result', code=result['pickup_code']))
            st.write(t('notification'))
            st.caption(t('preview_only'))
    with st.container(key='center_back'):
        home_button()


def collect_page(controller):
    heading(t('collect'), True)
    with st.container(key='narrow_form'):
        code = st.text_input(t('code_label'), key='pickup_code', max_chars=6,
                             placeholder=t('code_hint'), on_change=invalidate_code)
        if st.button(t('verify'), type='primary', key='verify_code'):
            invalidate_code()
            try:
                controller.verify(code)
                st.session_state['verified_code'] = code.strip()
            except (ValueError, StorageError) as error:
                st.session_state['collect_error'] = str(error)
    if verified := st.session_state.get('verified_code'):
        try:
            parcel = controller.verify(verified)
        except (ValueError, StorageError) as error:
            st.session_state.pop('verified_code', None)
            st.session_state['collect_error'] = str(error)
        else:
            st.divider()
            with st.container(key='collection_result'):
                heading(t('verified'), True)
                st.html(f'<p class="center-copy">{escape(t("location", number=parcel.locker_id))}</p>'
                        f'<p class="center-copy">{escape(t("take"))}</p>')
                if st.button(t('confirm'), type='primary', key='confirm_collection'):
                    try:
                        controller.collect(verified)
                        st.session_state.pop('verified_code', None)
                        st.session_state.pop('collect_error', None)
                        st.session_state['collected'] = True
                        st.rerun()
                    except (ValueError, StorageError) as error:
                        st.session_state['collect_error'] = str(error)
    if message := st.session_state.get('collect_error'):
        show_error(message)
    if st.session_state.get('collected'):
        st.divider()
        with st.container(key='collection_result'):
            heading(t('collected'), True)
            st.html(f'<p class="center-copy">{escape(t("released"))}</p>')
    with st.container(key='center_back'):
        home_button()
    st.html(f'<p class="simulation-note">{escape(t("simulation"))}</p>')


def records_page(controller):
    heading(t('records'))
    st.html(f'<p class="page-description">{escape(t("records_desc"))}</p>')
    parcels = controller.parcels()
    if not parcels:
        st.info(t('empty'))
    else:
        rows = ''.join(
            '<tr>' + ''.join(f'<td>{escape(str(value))}</td>' for value in (
                p.parcel_id, p.tracking_number, p.get_recipient_name(),
                f'{p.locker_id:02d}', t(p.status)
            )) + '</tr>' for p in parcels
        )
        headers = ''.join(f'<th scope="col">{escape(t(key))}</th>'
                          for key in ('id', 'tracking', 'recipient', 'locker', 'status'))
        st.html('<div class="table-scroll"><table class="parcel-table">'
                f'<caption class="sr-only">{escape(t("records"))}</caption>'
                f'<thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div>')
        stored = sum(p.is_stored() for p in parcels)
        st.write(t('records_summary', total=len(parcels), stored=stored, collected=len(parcels) - stored))
    home_button()


def lockers_page(controller):
    heading(t('lockers'))
    lockers = controller.lockers()
    available = sum(locker.is_available() for locker in lockers)
    summary = t('lockers_summary', total=len(lockers), available=available, occupied=len(lockers) - available)
    st.html(f'<p class="locker-summary">{escape(summary)}</p>')
    cards = ''.join(
        f'<div class="locker {"available" if locker.is_available() else "occupied"}">'
        f'<strong>{escape(t("locker_number", number=locker.locker_id))}</strong>'
        f'<span>{escape(t(locker.get_status()))}</span></div>'
        for locker in lockers
    )
    st.html(f'<div class="locker-grid">{cards}</div>')
    home_button()


def home_page():
    heading(t('welcome'), True)
    st.html(f'<p class="center-copy">{escape(t("choose"))}</p>')
    with st.container(key='narrow_form'):
        st.button(t('collect'), type='primary', use_container_width=True,
                  on_click=navigate, args=('collect',), key='home_collect')
        st.divider()
        st.caption(t('staff_group'))
        for page in ('register', 'records', 'lockers'):
            st.button(t(page), use_container_width=True,
                      on_click=navigate, args=(page,), key=f'home_{page}')


def run_app():
    st.session_state.setdefault('language', 'zh')
    st.session_state.setdefault('page', 'home')
    st.set_page_config(page_title=t('app_title'), layout='wide', initial_sidebar_state='expanded')
    st.html(f'<style>{Path(__file__).with_name("styles.css").read_text(encoding="utf-8")}</style>')
    with st.sidebar:
        st.selectbox('语言 / Language', ('zh', 'en'),
                     format_func=lambda value: {'zh': '简体中文', 'en': 'English'}[value],
                     key='language')
        st.subheader(t('nav'))
        page_labels = {key: t(key) for key in PAGES}
        page = st.radio(t('pages'), PAGES, format_func=page_labels.__getitem__, key='page',
                        on_change=clear_flow, label_visibility='collapsed')
        st.divider()
        st.caption(t('local'))
    role = {'register': 'courier', 'collect': 'customer', 'records': 'staff', 'lockers': 'staff'}.get(page)
    st.html(f'<header class="app-header"><h1>{escape(t("app_title"))}</h1>'
            f'<span>{escape(t(role)) if role else ""}</span></header>')
    controller = ParcelController()
    try:
        if page == 'home':
            home_page()
        else:
            {'register': register_page, 'collect': collect_page,
             'records': records_page, 'lockers': lockers_page}[page](controller)
    except StorageError as error:
        show_error(str(error))
    st.html(f'<footer class="app-footer">{escape(t("footer"))}</footer>')
