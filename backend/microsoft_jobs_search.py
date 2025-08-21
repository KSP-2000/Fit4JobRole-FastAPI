import argparse
from playwright.sync_api import sync_playwright
from utils import append_to_json_file

DEBUG = True
MAX_JOBS = 3

def find_microsoft_jobs(role="Python Developer", location="Hyderabad", max_pages=1):
    job_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=500) # Use headless=False while testing
        context = browser.new_context()
        page = context.new_page()

        # Go to base search page
        page.goto("https://careers.microsoft.com/us/en/search-results")
        page.wait_for_selector("input#search-box8", timeout=10000)

        page.fill("input#search-box8", role)
        page.fill("input#location-box11", location)

        page.get_by_role("button", name="Find jobs").click()

        page.wait_for_timeout(timeout=3000)

        page.wait_for_selector("[role='listitem']", timeout=15000)
        job_tiles = page.locator("[role='listitem']")
        total_jobs = job_tiles.count()
       
        page_num = 0

        # To Limit max number of jobs search while testing
        global MAX_JOBS
        if DEBUG == False:
            MAX_JOBS = float("inf")

        while page_num < max_pages:
            page.wait_for_selector("[role='listitem']", timeout=15000)
            job_tiles = page.locator("[role='listitem']")
            total_jobs = job_tiles.count()
            
            for i in range(min(MAX_JOBS, total_jobs)):
                job_tiles.nth(i).click()
                page.wait_for_selector("h1", timeout=15000)

                job = {}

                # Title
                job["title"] = page.locator("h1").first.inner_text()

                # Location
                try:
                    location_text = page.locator("div.ms-Stack-inner p").first.inner_text()
                except:
                    location_text = "Not Found"
                job["location"] = location_text

                # Description from 3 sections
                sections = ["Overview", "Responsibilities", "Qualifications"]
                description_parts = []

                for section in sections:
                    try:
                        heading = page.locator(f"h3:has-text('{section}')").first
                        sibling_elements = heading.evaluate_handle(
                            """el => {
                                const content = [];
                                let node = el.nextElementSibling;
                                while (node && node.tagName !== 'H3') {
                                    content.push(node.innerText);
                                    node = node.nextElementSibling;
                                }
                                return content;
                            }"""
                        )
                        content = sibling_elements.json_value()
                        description_parts.append(f"{section}:\n" + "\n".join(content))
                    except:
                        continue

                job["description"] = "\n\n".join(description_parts).strip() or "Not Available"

                # Static fields
                job["company_name"] = "Microsoft"
                job["salary"] = "Not disclosed"
                job["job_link"] = page.url
                job["source"] = "Microsoft Careers"

                job_list.append(job)

                # Go back and wait
                page.go_back()
                page.wait_for_selector("[role='listitem']", timeout=10000)
                job_tiles = page.locator("[role='listitem']")

            # Move to next page
            try:
                next_button = page.get_by_role("button", name="Next")
                if next_button.is_visible():
                    next_button.click()
                    page.wait_for_timeout(3000)
                    page_num += 1
                else:
                    break
            except:
                break


        browser.close()
    return job_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Microsoft jobs.")
    parser.add_argument("--role", type=str, default="Python Developer", help="Job role to search")
    parser.add_argument("--location", type=str, default="Hyderabad", help="Location to search")
    parser.add_argument("--pages", type=int, default=1, help="Maximum number of pages to search")
    parser.add_argument("--output", type=str, default="microsoft_jobs.json", help="Output JSON file name")

    args = parser.parse_args()

    all_jobs = find_microsoft_jobs(role=args.role, location=args.location, max_pages=args.pages)
    append_to_json_file(all_jobs, args.output)

