"""Streamlit app."""

import streamlit as st


def main():
    """Main function."""
    # main page config
    st.set_page_config(page_title="Minifigures Webshop", page_icon="🏠")

    st.title("🏠 Minifigures Webshop")  # type: ignore[no-untyped-call]
    st.write("This is a mock-up for a simple marketplace for LEGO pieces.")
    st.markdown("---")
    st.markdown("### 👈 Pages")
    st.markdown(" - **🎭 Product**: Upload and view your product")
    st.markdown(" - **💰 Market**: Go to our marketplace")


if __name__ == "__main__":
    main()
