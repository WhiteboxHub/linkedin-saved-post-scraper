# import os
# import time
# import json
# import re
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

# # ------------------------------
# # 1️⃣ Load LinkedIn Credentials
# # ------------------------------
# with open("credentials.json", "r") as f:
#     creds = json.load(f)

# USERNAME = creds["username"]
# PASSWORD = creds["password"]

# # ------------------------------
# # 2️⃣ Selenium Setup
# # ------------------------------
# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-notifications")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ------------------------------
# # 3️⃣ Login
# # ------------------------------
# print("🔐 Logging into LinkedIn...")
# driver.get("https://www.linkedin.com/login")
# time.sleep(2)

# driver.find_element(By.ID, "username").send_keys(USERNAME)
# driver.find_element(By.ID, "password").send_keys(PASSWORD)
# driver.find_element(By.XPATH, "//button[@type='submit']").click()

# time.sleep(5)
# print("✅ Login successful!")

# # ------------------------------
# # 4️⃣ Open Saved Posts Page
# # ------------------------------
# driver.get("https://www.linkedin.com/my-items/saved-posts/")
# time.sleep(5)

# # Scroll multiple times to load posts
# for i in range(5):
#     driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
#     time.sleep(3)

# # ------------------------------
# # 🧩 NEW: Expand all "See more" buttons
# # ------------------------------
# see_more_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'See more')]")
# print(f"📖 Found {len(see_more_buttons)} 'See more' buttons")

# for btn in see_more_buttons:
#     try:
#         driver.execute_script("arguments[0].scrollIntoView(true);", btn)
#         time.sleep(0.5)
#         btn.click()
#         time.sleep(0.5)
#     except (ElementClickInterceptedException, ElementNotInteractableException):
#         driver.execute_script("arguments[0].click();", btn)
#     except Exception as e:
#         print(f"⚠️ Could not click button: {e}")

# time.sleep(2)  # allow expanded text to load

# # Now parse with BeautifulSoup after expansion
# soup = BeautifulSoup(driver.page_source, "html.parser")

# # ------------------------------
# # 5️⃣ Extract Posts
# # ------------------------------
# posts = soup.find_all("div", class_="entity-result__content-container")
# print(f"🧾 Found {len(posts)} saved posts")

# save_dir = "LinkedIn_Saved_Posts"
# os.makedirs(save_dir, exist_ok=True)

# # ------------------------------
# # 6️⃣ Parse Each Post
# # ------------------------------
# for idx, post in enumerate(posts, start=1):
#     post_folder = os.path.join(save_dir, f"Post_{idx}")
#     os.makedirs(post_folder, exist_ok=True)

#     # Extract post link
#     link_tag = post.find("a", attrs={"data-test-app-aware-link": True}, href=True)
#     post_link = link_tag["href"] if link_tag else None

#     # Extract author name
#     author_tag = post.find("span", dir="ltr")
#     author = author_tag.get_text(strip=True) if author_tag else "Unknown Author"

#     # Extract post text (after “See more” expansion)
#     text_tag = post.find("p", class_=re.compile("entity-result__content-summary"))
#     if not text_tag:
#         # fallback for expanded post body
#         text_tag = post.find("div", class_=re.compile("feed-shared-update-v2__description"))
#     post_text = text_tag.get_text(separator="\n", strip=True) if text_tag else "No content found"

#     # Extract image(s)
#     image_tags = post.find_all("img", src=True)
#     image_urls = [img["src"] for img in image_tags if "profile" not in img["src"]]

#     # Save text
#     with open(os.path.join(post_folder, "post.txt"), "w", encoding="utf-8") as f:
#         f.write(f"Author: {author}\n\n")
#         f.write(f"Link: {post_link}\n\n")
#         f.write(post_text)

#     # Save link
#     if post_link:
#         with open(os.path.join(post_folder, "link.txt"), "w", encoding="utf-8") as f:
#             f.write(post_link)

#     # Download images
#     for i, url in enumerate(image_urls, start=1):
#         try:
#             img_data = requests.get(url).content
#             img_path = os.path.join(post_folder, f"image_{i}.jpg")
#             with open(img_path, "wb") as img_file:
#                 img_file.write(img_data)
#         except Exception as e:
#             print(f"⚠️ Could not download image {url}: {e}")

#     print(f"✅ Saved Post {idx}: {author}")

# driver.quit()
# print("🎉 All saved posts downloaded successfully!")



# import os
# import time
# import json
# import re
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
# from webdriver_manager.chrome import ChromeDriverManager

# # ------------------------------
# # 1️⃣ Load LinkedIn Credentials
# # ------------------------------
# with open("credentials.json", "r") as f:
#     creds = json.load(f)

# USERNAME = creds["username"]
# PASSWORD = creds["password"]

# # ------------------------------
# # 2️⃣ Selenium Setup
# # ------------------------------
# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-notifications")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ------------------------------
# # 3️⃣ Login
# # ------------------------------
# print("🔐 Logging into LinkedIn...")
# driver.get("https://www.linkedin.com/login")
# time.sleep(2)

# driver.find_element(By.ID, "username").send_keys(USERNAME)
# driver.find_element(By.ID, "password").send_keys(PASSWORD)
# driver.find_element(By.XPATH, "//button[@type='submit']").click()
# time.sleep(5)
# print("✅ Login successful!")

# # ------------------------------
# # 4️⃣ Load all saved posts (scroll + click "Show more results")
# # ------------------------------
# print("⬇️ Scrolling and loading all saved posts...")

# driver.get("https://www.linkedin.com/my-items/saved-posts/")
# time.sleep(5)

# scroll_pause = 3
# retry_attempts = 3
# last_height = driver.execute_script("return document.body.scrollHeight")
# same_height_count = 0

# while True:
#     driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
#     time.sleep(scroll_pause)

#     # Try clicking “Show more results”
#     try:
#         show_more_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Show more results')]/ancestor::button")
#         driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
#         time.sleep(1)
#         show_more_button.click()
#         print("➡️ Clicked 'Show more results'")
#         time.sleep(4)
#     except Exception:
#         pass

#     # Check if new content loaded
#     new_height = driver.execute_script("return document.body.scrollHeight")

#     if new_height == last_height:
#         same_height_count += 1
#         if same_height_count >= retry_attempts:
#             print("✅ All posts loaded (no more new content).")
#             break
#         else:
#             print(f"⚠️ No new posts yet... retrying ({same_height_count}/{retry_attempts})")
#             time.sleep(5)
#     else:
#         same_height_count = 0  # reset counter
#     last_height = new_height

#     if same_height_count % 5 == 0:
#         print("⏳ Cooling down to avoid rate-limiting...")
#         time.sleep(5)

# # ------------------------------
# # 5️⃣ Expand all “See more” buttons
# # ------------------------------
# see_more_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'See more')]")
# print(f"📖 Found {len(see_more_buttons)} 'See more' buttons")

# for btn in see_more_buttons:
#     try:
#         driver.execute_script("arguments[0].scrollIntoView(true);", btn)
#         time.sleep(0.5)
#         btn.click()
#         time.sleep(0.5)
#     except (ElementClickInterceptedException, ElementNotInteractableException):
#         try:
#             driver.execute_script("arguments[0].click();", btn)
#         except Exception:
#             pass
#     except Exception as e:
#         print(f"⚠️ Could not click button: {e}")

# time.sleep(2)

# # ------------------------------
# # 6️⃣ Parse HTML with BeautifulSoup
# # ------------------------------
# soup = BeautifulSoup(driver.page_source, "html.parser")

# posts = soup.find_all("div", class_="entity-result__content-container")
# print(f"🧾 Found {len(posts)} saved posts")

# save_dir = "LinkedIn_Saved_Posts"
# os.makedirs(save_dir, exist_ok=True)

# # ------------------------------
# # 7️⃣ Extract & Save Each Post
# # ------------------------------
# for idx, post in enumerate(posts, start=1):
#     post_folder = os.path.join(save_dir, f"Post_{idx}")
#     os.makedirs(post_folder, exist_ok=True)

#     # --- Author ---
#     author_tag = post.find("span", dir="ltr")
#     author = author_tag.get_text(strip=True) if author_tag else "Unknown Author"

#     # --- Post link ---
#     link_tag = post.find("a", attrs={"data-test-app-aware-link": True}, href=True)
#     post_link = link_tag["href"] if link_tag else None

#     # --- Post text ---
#     text_tag = post.find("p", class_=re.compile("entity-result__content-summary"))
#     if not text_tag:
#         text_tag = post.find("div", class_=re.compile("feed-shared-update-v2__description"))
#     post_text = text_tag.get_text(separator="\n", strip=True) if text_tag else "No content found"

#     # --- Links inside post body ---
#     body_links = [a["href"] for a in post.find_all("a", href=True) if a["href"].startswith("http")]
#     body_links = list(set(body_links))  # remove duplicates

#     # --- Images ---
#     image_tags = post.find_all("img", src=True)
#     image_urls = [img["src"] for img in image_tags if "profile" not in img["src"]]

#     # --- Save Text ---
#     with open(os.path.join(post_folder, "post.txt"), "w", encoding="utf-8") as f:
#         f.write(f"Author: {author}\n\n")
#         f.write(f"Link: {post_link}\n\n")
#         f.write(post_text)
#         if body_links:
#             f.write("\n\nEmbedded Links:\n" + "\n".join(body_links))

#     # --- Save Link File ---
#     if post_link:
#         with open(os.path.join(post_folder, "link.txt"), "w", encoding="utf-8") as f:
#             f.write(post_link)

#     # --- Download Images ---
#     for i, url in enumerate(image_urls, start=1):
#         try:
#             img_data = requests.get(url).content
#             img_path = os.path.join(post_folder, f"image_{i}.jpg")
#             with open(img_path, "wb") as img_file:
#                 img_file.write(img_data)
#         except Exception as e:
#             print(f"⚠️ Could not download image {url}: {e}")

#     print(f"✅ Saved Post {idx}: {author}")

# driver.quit()
# print("🎉 All saved posts downloaded successfully!")


#=-----------------------------------------------------pdf, docs code-------------------------------

# import os
# import time
# import json
# import re
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
# from webdriver_manager.chrome import ChromeDriverManager

# # ------------------------------
# # 1️⃣ Load LinkedIn Credentials
# # ------------------------------
# with open("credentials.json", "r") as f:
#     creds = json.load(f)

# USERNAME = creds["username"]
# PASSWORD = creds["password"]

# # ------------------------------
# # 2️⃣ Selenium Setup
# # ------------------------------
# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument("--disable-notifications")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # ------------------------------
# # 3️⃣ Login
# # ------------------------------
# print("🔐 Logging into LinkedIn...")
# driver.get("https://www.linkedin.com/login")
# time.sleep(2)

# driver.find_element(By.ID, "username").send_keys(USERNAME)
# driver.find_element(By.ID, "password").send_keys(PASSWORD)
# driver.find_element(By.XPATH, "//button[@type='submit']").click()
# time.sleep(5)
# print("✅ Login successful!")

# # ------------------------------
# # 4️⃣ Load all saved posts (scroll + click "Show more results")
# # ------------------------------
# print("⬇️ Scrolling and loading all saved posts...")

# driver.get("https://www.linkedin.com/my-items/saved-posts/")
# time.sleep(5)

# scroll_pause = 3
# retry_attempts = 3
# last_height = driver.execute_script("return document.body.scrollHeight")
# same_height_count = 0

# while True:
#     driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
#     time.sleep(scroll_pause)

#     # Try clicking “Show more results”
#     try:
#         show_more_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Show more results')]/ancestor::button")
#         driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
#         time.sleep(1)
#         show_more_button.click()
#         print("➡️ Clicked 'Show more results'")
#         time.sleep(4)
#     except Exception:
#         pass

#     # Check if new content loaded
#     new_height = driver.execute_script("return document.body.scrollHeight")

#     if new_height == last_height:
#         same_height_count += 1
#         if same_height_count >= retry_attempts:
#             print("✅ All posts loaded (no more new content).")
#             break
#         else:
#             print(f"⚠️ No new posts yet... retrying ({same_height_count}/{retry_attempts})")
#             time.sleep(5)
#     else:
#         same_height_count = 0
#     last_height = new_height

# # ------------------------------
# # 5️⃣ Expand all “See more” buttons
# # ------------------------------
# see_more_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'See more')]")
# print(f"📖 Found {len(see_more_buttons)} 'See more' buttons")

# for btn in see_more_buttons:
#     try:
#         driver.execute_script("arguments[0].scrollIntoView(true);", btn)
#         time.sleep(0.5)
#         btn.click()
#         time.sleep(0.5)
#     except (ElementClickInterceptedException, ElementNotInteractableException):
#         try:
#             driver.execute_script("arguments[0].click();", btn)
#         except Exception:
#             pass
#     except Exception as e:
#         print(f"⚠️ Could not click button: {e}")

# time.sleep(2)

# # ------------------------------
# # 6️⃣ Parse HTML with BeautifulSoup
# # ------------------------------
# soup = BeautifulSoup(driver.page_source, "html.parser")

# posts = soup.find_all("div", class_="entity-result__content-container")
# print(f"🧾 Found {len(posts)} saved posts")

# save_dir = "LinkedIn_Saved_Posts"
# os.makedirs(save_dir, exist_ok=True)

# # ------------------------------
# # 7️⃣ Extract & Save Each Post
# # ------------------------------
# for idx, post in enumerate(posts, start=1):
#     post_folder = os.path.join(save_dir, f"Post_{idx}")
#     os.makedirs(post_folder, exist_ok=True)

#     # --- Author ---
#     author_tag = post.find("span", dir="ltr")
#     author = author_tag.get_text(strip=True) if author_tag else "Unknown Author"

#     # --- Post link ---
#     link_tag = post.find("a", attrs={"data-test-app-aware-link": True}, href=True)
#     post_link = link_tag["href"] if link_tag else None

#     # --- Post text ---
#     text_tag = post.find("p", class_=re.compile("entity-result__content-summary"))
#     if not text_tag:
#         text_tag = post.find("div", class_=re.compile("feed-shared-update-v2__description"))
#     post_text = text_tag.get_text(separator="\n", strip=True) if text_tag else "No content found"

#     # --- Links inside post body ---
#     body_links = [a["href"] for a in post.find_all("a", href=True) if a["href"].startswith("http")]
#     body_links = list(set(body_links))  # remove duplicates

#     # --- Normal images ---
#     image_tags = post.find_all("img", src=True)
#     image_urls = [img["src"] for img in image_tags if "profile" not in img["src"]]

#     # --- Document/PDF carousel images ---
#     doc_slides = post.find_all("li", class_=re.compile("carousel-slide"))
#     doc_images = []
#     for slide in doc_slides:
#         img_tag = slide.find("img", src=True)
#         if img_tag and "media.licdn.com" in img_tag["src"]:
#             doc_images.append(img_tag["src"])

#     # --- Save Text ---
#     with open(os.path.join(post_folder, "post.txt"), "w", encoding="utf-8") as f:
#         f.write(f"Author: {author}\n\n")
#         f.write(f"Link: {post_link}\n\n")
#         f.write(post_text)
#         if body_links:
#             f.write("\n\nEmbedded Links:\n" + "\n".join(body_links))

#     # --- Save Link File ---
#     if post_link:
#         with open(os.path.join(post_folder, "link.txt"), "w", encoding="utf-8") as f:
#             f.write(post_link)

#     # --- Download regular images ---
#     for i, url in enumerate(image_urls, start=1):
#         try:
#             img_data = requests.get(url).content
#             img_path = os.path.join(post_folder, f"image_{i}.jpg")
#             with open(img_path, "wb") as img_file:
#                 img_file.write(img_data)
#         except Exception as e:
#             print(f"⚠️ Could not download image {url}: {e}")

#     # --- Download document images ---
#     for j, url in enumerate(doc_images, start=1):
#         try:
#             img_data = requests.get(url).content
#             img_path = os.path.join(post_folder, f"document_page_{j}.jpg")
#             with open(img_path, "wb") as img_file:
#                 img_file.write(img_data)
#         except Exception as e:
#             print(f"⚠️ Could not download document page {url}: {e}")

#     print(f"✅ Saved Post {idx}: {author} ({len(image_urls)} images, {len(doc_images)} docs)")

# driver.quit()
# print("🎉 All saved posts downloaded successfully!")



#---------------------- implemented different extracts-----------------------------------------------------------------

import os
import time
import json
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------
# 1️⃣ Load LinkedIn Credentials
# ------------------------------
with open("credentials.json", "r") as f:
    creds = json.load(f)

USERNAME = creds["username"]
PASSWORD = creds["password"]

# ------------------------------
# 2️⃣ Selenium Setup
# ------------------------------
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ------------------------------
# 3️⃣ Login
# ------------------------------
print("🔐 Logging into LinkedIn...")
driver.get("https://www.linkedin.com/login")
time.sleep(2)

driver.find_element(By.ID, "username").send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(5)
print("✅ Login successful!")

# ------------------------------
# 4️⃣ Load all saved posts (scroll + click "Show more results")
# ------------------------------
print("⬇️ Scrolling and loading all saved posts...")

driver.get("https://www.linkedin.com/my-items/saved-posts/")
time.sleep(5)

scroll_pause = 3
retry_attempts = 3
last_height = driver.execute_script("return document.body.scrollHeight")
same_height_count = 0

while True:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(scroll_pause)

    # Try clicking “Show more results”
    try:
        show_more_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Show more results')]/ancestor::button")
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
        time.sleep(1)
        show_more_button.click()
        print("➡️ Clicked 'Show more results'")
        time.sleep(4)
    except Exception:
        pass

    # Check if new content loaded
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        same_height_count += 1
        if same_height_count >= retry_attempts:
            print("✅ All posts loaded (no more new content).")
            break
        else:
            print(f"⚠️ No new posts yet... retrying ({same_height_count}/{retry_attempts})")
            time.sleep(5)
    else:
        same_height_count = 0
    last_height = new_height

# ------------------------------
# 5️⃣ Expand all “See more” buttons
# ------------------------------
see_more_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'See more')]")
print(f"📖 Found {len(see_more_buttons)} 'See more' buttons")

for btn in see_more_buttons:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.5)
        btn.click()
        time.sleep(0.5)
    except (ElementClickInterceptedException, ElementNotInteractableException):
        try:
            driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass
    except Exception as e:
        print(f"⚠️ Could not click button: {e}")

time.sleep(2)

# ------------------------------
# 6️⃣ Parse HTML with BeautifulSoup
# ------------------------------
soup = BeautifulSoup(driver.page_source, "html.parser")

posts = soup.find_all("div", class_="entity-result__content-container")
print(f"🧾 Found {len(posts)} saved posts")

save_dir = "LinkedIn_Saved_Posts"
os.makedirs(save_dir, exist_ok=True)

# ------------------------------
# 7️⃣ Helper Function - Robust Text Extraction
# ------------------------------
def extract_post_text(post):
    """
    Tries multiple fallback selectors to extract text from all types of LinkedIn posts.
    """
    selectors = [
        ("p", re.compile("entity-result__content-summary")),        # text-only posts
        ("div", re.compile("feed-shared-update-v2__description")),  # image/link shares
        ("div", re.compile("feed-shared-text-view__text")),         # new LinkedIn layout
        ("span", re.compile("break-words")),                        # span text blocks
        ("span", {"dir": "ltr"}),                                   # fallback for author-post format
    ]
    
    for tag, pattern in selectors:
        if isinstance(pattern, re.Pattern):
            el = post.find(tag, class_=pattern)
        elif isinstance(pattern, dict):
            el = post.find(tag, attrs=pattern)
        else:
            el = post.find(tag, pattern)
        if el and el.get_text(strip=True):
            return el.get_text(separator="\n", strip=True)
    return "No content found"

# ------------------------------
# 8️⃣ Extract & Save Each Post
# ------------------------------
for idx, post in enumerate(posts, start=1):
    post_folder = os.path.join(save_dir, f"Post_{idx}")
    os.makedirs(post_folder, exist_ok=True)

    # --- Author ---
    author_tag = post.find("span", dir="ltr")
    author = author_tag.get_text(strip=True) if author_tag else "Unknown Author"

    # --- Post link ---
    link_tag = post.find("a", attrs={"data-test-app-aware-link": True}, href=True)
    post_link = link_tag["href"] if link_tag else None

    # --- Post text (robust extraction) ---
    post_text = extract_post_text(post)

    # --- Links inside post body ---
    body_links = [a["href"] for a in post.find_all("a", href=True) if a["href"].startswith("http")]
    body_links = list(set(body_links))  # remove duplicates

    # --- Normal images ---
    image_tags = post.find_all("img", src=True)
    image_urls = [img["src"] for img in image_tags if "profile" not in img["src"]]

    # --- Document/PDF carousel images ---
    doc_slides = post.find_all("li", class_=re.compile("carousel-slide"))
    doc_images = []
    for slide in doc_slides:
        img_tag = slide.find("img", src=True)
        if img_tag and "media.licdn.com" in img_tag["src"]:
            doc_images.append(img_tag["src"])

    # --- Save Text ---
    with open(os.path.join(post_folder, "post.txt"), "w", encoding="utf-8") as f:
        f.write(f"Author: {author}\n\n")
        f.write(f"Link: {post_link}\n\n")
        f.write(post_text)
        if body_links:
            f.write("\n\nEmbedded Links:\n" + "\n".join(body_links))

    # --- Save Link File ---
    if post_link:
        with open(os.path.join(post_folder, "link.txt"), "w", encoding="utf-8") as f:
            f.write(post_link)

    # --- Download regular images ---
    for i, url in enumerate(image_urls, start=1):
        try:
            img_data = requests.get(url).content
            img_path = os.path.join(post_folder, f"image_{i}.jpg")
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
        except Exception as e:
            print(f"⚠️ Could not download image {url}: {e}")

    # --- Download document images ---
    for j, url in enumerate(doc_images, start=1):
        try:
            img_data = requests.get(url).content
            img_path = os.path.join(post_folder, f"document_page_{j}.jpg")
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
        except Exception as e:
            print(f"⚠️ Could not download document page {url}: {e}")

    print(f"✅ Saved Post {idx}: {author} ({len(image_urls)} images, {len(doc_images)} docs)")

# ------------------------------
# 9️⃣ Done
# ------------------------------
driver.quit()
print("🎉 All saved posts downloaded successfully!")
