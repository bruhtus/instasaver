import re
import os
import tempfile
import instaloader
import base64
import streamlit as st

from fire import Fire
from zipfile import ZipFile

def main():
    st.title('Instasaver')
    st.markdown("Save your chosen instagram's post (public profile only)")
    with tempfile.TemporaryDirectory() as temp:
        load = instaloader.Instaloader(
                dirname_pattern=temp,
                download_comments=False,
                download_geotags=False,
                download_video_thumbnails=False,
                save_metadata=False)

        url_input = st.text_input('Post Url')
        
        try:
            if url_input:
                load.post_metadata_txt_pattern = ''
                shortcode = url_to_short_code(url_input)
                check_post_url(load, shortcode, temp)
        
        except AttributeError:
            st.write("It seems like it's not a url")

        except KeyError:
            st.write("It seems like it's a private account")

def url_to_short_code(post_url):
    regexp = '^(?:.*\/(p|tv)\/)([\d\w\-_]+)'
    post_short_code = re.search(regexp, post_url).group(2)
    print('From url {} extracted shorcode:{}'.format(post_url, post_short_code))
    print(f'shotcode: {post_short_code}')
    return post_short_code

def check_post_url(loader, shortcode, temp):
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target=temp)
    file_list = [filename for filename in os.listdir(temp)]
    if len(file_list) == 1:
        try:
            st.image(f'{temp}/{file_list[0]}', use_column_width=True)
            st.markdown(download_button(f'{temp}/{file_list[0]}', temp), unsafe_allow_html=True)

        except:
            st.video(f'{temp}/{file_list[0]}')
            st.markdown(download_button(f'{temp}/{file_list[0]}', temp), unsafe_allow_html=True)

    else:
        for filename in file_list:
            try:
                st.image(f'{temp}/{filename}', use_column_width=True)
                st.markdown(download_button(f'{temp}/{filename}', temp), unsafe_allow_html=True)

            except:
                st.video(f'{temp}/{filename}')
                st.markdown(download_button(f'{temp}/{filename}', temp), unsafe_allow_html=True)

def download_button(bin_file, temp):
    with open(bin_file, 'rb') as f:
        data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download here</a>'
        return href

if __name__ == '__main__':
    Fire(main)
