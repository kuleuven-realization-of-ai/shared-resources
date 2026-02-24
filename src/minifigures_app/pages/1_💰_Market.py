"""Marketplace page."""

from math import ceil

import streamlit as st
from PIL import Image, ImageOps

from minifigures_app.utils import get_image, list_im_tags


def main():
    """Main function."""
    st.set_page_config(
        page_title="Market",
        page_icon="💰",
    )

    # page description
    st.title("💰 Market")
    st.markdown("---")

    # Ensure clean session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0

    # get images
    image_tags = list_im_tags()

    # paginate results
    image_slice = image_tags[
        st.session_state.current_page
        * 9 : min(st.session_state.current_page * 9 + 9, len(image_tags))
    ]
    n_rows = ceil(len(image_slice) / 3)
    for row in range(n_rows):
        for i, col in enumerate(st.columns(3)):
            try:
                image_tag = image_slice[row * 3 + i]
                image = get_image(image_tag)

                col.write(image_tag)
                col.image(_rescale_image(image, resolution=200))
                col.button(
                    "View",
                    key=image_tag,
                    on_click=lambda x: st.error("Not yet implemented"),
                    args=(image_tag,),
                )
            except Exception:
                continue

    # paging buttons
    st.markdown("""---""")
    cols = st.columns(5)
    cols[2].text(f"Page: {st.session_state.current_page + 1} / {ceil(len(image_tags) / 9)}")

    # If I am not at the beginning
    if (
        image_tags
        and (st.session_state.current_page != 0)
        and (_ := cols[0].button("Previous Page"))
    ):
        st.session_state.current_page -= 1
        st.experimental_rerun()

    # If I am not in the end
    if image_tags and (len(image_slice) == 9) and (_ := cols[-1].button("Next Page")):
        st.session_state.current_page += 1
        st.experimental_rerun()


def _rescale_image(im: Image.Image, resolution: int) -> Image.Image:
    """Rescale image to specified resolution."""
    size = (resolution, resolution)
    return ImageOps.pad(ImageOps.contain(im, size=size), size=size, color="white")


if __name__ == "__main__":
    main()
