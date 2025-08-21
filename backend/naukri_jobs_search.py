from playwright.sync_api import sync_playwright
from utils import append_to_json_file
import argparse

WORK_EXPERIENCE = "1" # use number of years -- whole numbers only(0,1,2,...)
DEBUG = True
MAX_JOBS = 3

def search_naukri_jobs(role="Python Developer", location="Hyderabad", max_pages=1):
    jobs_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=500) # Use headless=False while testing
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.naukri.com/")
        
        page.fill("input[placeholder = 'Enter skills / designations / companies']", role)

        page.fill("input[placeholder = 'Enter location']", location)

        page.locator("div.qsbExperience").click()
        page.wait_for_selector("ul.dropdown li", timeout=2000)

        page.locator("ul.dropdown li").nth(WORK_EXPERIENCE).click()

        page.locator("div.qsbSubmit").click()
        page.wait_for_selector("div.cust-job-tuple", timeout=5000)

        cur_page = 1

        while cur_page <= max_pages:

            jobs = page.locator("div.cust-job-tuple").all()

            temp_max_jobs = MAX_JOBS

            for job in jobs:
                #To limit number of jobs while testing 
                if DEBUG == True:
                    if temp_max_jobs>0:
                        temp_max_jobs-=1
                    else:
                        break

                title = job.locator("a.title").inner_text().strip()
                company = job.locator("a.comp-name").inner_text().strip()
                location = job.locator("span.loc-wrap").inner_text().strip()

                salary_locator = job.locator("span.sal-wrap")
                salary = salary_locator.inner_text() if salary_locator.count() else "Not disclosed"

                link = job.locator("a.title").get_attribute("href")

                # Open Each job tile for full Job Description
                job_full_page = browser.new_page()
                job_full_page.goto(link)
                job_full_page.wait_for_timeout(2000)

                try:
                    description = job_full_page.locator("section.styles_job-desc-container__txpYf").inner_text()
                except:
                    description = "N/A"

                job_full_page.close()

                result = {
                    "title" : title,
                    "location": location,
                    "description": description,
                    "company_name": company,
                    "salary": salary,
                    "job_link": link,
                    "source": "Naukri"
                }

                jobs_list.append(result)

            # page.wait_for_timeout(2000)

            next_button = page.locator("div.pagination a:has-text('Next')")
            if next_button.count() > 0 and next_button.first.is_visible() and next_button.first.is_enabled():
                cur_page += 1
                next_button.first.click()
            else:
                break
        
        browser.close()
    
    return jobs_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Naukri jobs.")
    parser.add_argument("--role", type=str, default="Python Developer", help="Job role to search")
    parser.add_argument("--location", type=str, default="Hyderabad", help="Location to search")
    parser.add_argument("--pages", type=int, default=1, help="Maximum number of pages to search")
    parser.add_argument("--output", type=str, default="Naukri_jobs.json", help="Output JSON file name")

    args = parser.parse_args()

    all_jobs = search_naukri_jobs(role=args.role, location=args.location, max_pages=args.pages)

    append_to_json_file(all_jobs, args.output)


