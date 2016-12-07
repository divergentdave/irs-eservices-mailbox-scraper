#!/usr/bin/env python3
import mechanicalsoup
import os
import re
import shutil
import time
import urllib
import yaml

DIR = "files"
RE_JS = re.compile("^openWin\('(.*)'\)$")
RE_CONTENT_DISPOSITION = re.compile("^attachment; filename=(.*)$")


def main():
    os.makedirs(DIR, exist_ok=True)
    credentials = yaml.load(open("credentials.yaml"))

    br = mechanicalsoup.Browser(soup_config={"features": "lxml"})
    br.session.headers.update({"Accept-Language": "en-US,en;q=0.8"})

    signon_page = br.get("https://la.www4.irs.gov/PORTAL-PROD/CRM/signon.html")
    signon_form = signon_page.soup.form
    username_input = signon_form.select("input[name=USER]")[0]
    username_input["value"] = credentials["username"]
    password_input = signon_form.select("input[name=PASSWORD]")[0]
    password_input["value"] = credentials["password"]
    interstitial_page = br.submit(signon_form, signon_page.url)
    user_page = br.submit(interstitial_page.soup.form, interstitial_page.url)
    user_form = user_page.soup.form
    user_radio = user_page.soup.select("input[name=USER]")[-1]
    user_radio["checked"] = ""
    user_form.append(user_radio.extract())  # input was outside of form
    login_done_page = br.submit(user_form, user_page.url)
    refresh_content = login_done_page.soup.meta["content"]
    refresh_url = refresh_content[refresh_content.index("=") + 1:]
    refresh_url = urllib.parse.urljoin(login_done_page.url, refresh_url)
    br.get(refresh_url)

    list_page = br.get("https://la.www4.irs.gov/semail/views/list_mail")
    message_links = list_page.soup.find_all("a", text="Read")
    print("{} messages in mailbox".format(len(message_links)))
    for subject_link in list_page.soup.select("a.subject-link"):
        print("   {}".format(subject_link.text.strip()))
    for read_link in message_links:
        message_url = urllib.parse.urljoin(list_page.url, read_link["href"])
        message_page = br.get(message_url)
        download_links = message_page.soup.find_all("a", text="Download")
        print("{} attachments in message".format(len(download_links)))
        for download_link in download_links:
            match = RE_JS.match(download_link["onclick"])
            base_url = message_page.url
            download_url = urllib.parse.urljoin(base_url, match.group(1))
            br.get(download_url)
            time.sleep(4)
            file_dl_url = urllib.parse.urljoin(
                base_url,
                "/semail/servlet/FileDownload"
            )
            download_response = br.session.get(file_dl_url, stream=True)
            content_disp = download_response.headers["Content-Disposition"]
            match = RE_CONTENT_DISPOSITION.match(content_disp)
            filename = match.group(1)
            filename = os.path.basename(filename)  # just in case
            filename = os.path.join(DIR, filename)
            if os.path.isfile(filename):
                download_response.close()
                print("Skipping {}, already downloaded".format(filename))
            else:
                with open(filename, "wb") as f:
                    shutil.copyfileobj(download_response.raw, f)
                print("Downloaded to {}".format(filename))


if __name__ == "__main__":
    main()
