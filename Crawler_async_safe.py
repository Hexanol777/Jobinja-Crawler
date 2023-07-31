import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup

initial_url = 'https://jobinja.ir/jobs?&b=&filters%5Bjob_categories%5D%5B0%5D=&filters%5Bkeywords%5D%5B0%5D=&filters%5Blocations%5D%5B0%5D='

# Empty list to store job data dictionaries
job_data_list = []

async def fetch_page(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()


async def process_job_page(session, job_link):
    job_url = job_link['href']
    async with session.get(job_url) as job_response:
        if job_response.status == 200:
            job_soup = BeautifulSoup(await job_response.text(), 'html.parser')
            company_name_element = job_soup.find('h2', class_='c-companyHeader__name')

            # Get the company name (both Persian and English)
            company_name = company_name_element.text.strip().split('|')[0].strip()

            # Find the company meta information
            company_meta_elements = job_soup.find_all('span', class_='c-companyHeader__metaItem')

            # I wish whoever came up with this name tagging idea for the website a painful death I had
            # to start over two times after crawling through the entire website scraping 26k data because
            # around 2.5k entries (around 10% of data) in company category, size columns had their
            # values switched up together...
            if len(company_meta_elements) > 3:
                company_category = company_meta_elements[1].find('a', class_='c-companyHeader__metaLink').text.strip()
                company_size = company_meta_elements[2].text.strip()
                company_website = company_meta_elements[3].find('a', class_='c-companyHeader__metaLink').text.strip()
            else:
                # Get the company category (only the Persian phrase)
                company_category_element = company_meta_elements[0].find('a', class_='c-companyHeader__metaLink')
                company_category = company_category_element.text.strip() if company_category_element else ''

                # Get the company size (only the Persian phrase)
                company_size = company_meta_elements[1].text.strip() if len(company_meta_elements) > 1 else ''

                # Get the company website (if available)
                company_website_element = company_meta_elements[-1].find('a', class_='c-companyHeader__metaLink', target='_blank')
                company_website = company_website_element['href'].replace('https://', '').replace('http://', '').replace('/', '') if company_website_element else ''

            # Get the job position
            job_position_element = job_soup.find('div', class_='c-jobView__title').find('h1')
            job_position = job_position_element.text.strip() if job_position_element else ''

            # Pulling all 5 elements from the job info box
            info_box_element = job_soup.find('ul', class_='c-jobView__firstInfoBox c-infoBox').find_all('li', class_='c-infoBox__item')

            # Job category
            job_category = info_box_element[0].find('span', class_='black').text.strip()

            # Job location
            job_location = info_box_element[1].find('span', class_='black').text.strip().split('،')[0].strip()

            # Job employment type
            job_employment_type = info_box_element[2].find('span', class_='black').text.strip()

            # Job least experience needed
            job_experience = info_box_element[3].find('span', class_='black').text.strip()

            # Job salary
            job_salary = info_box_element[4].find('span', class_='black').text.strip() if len(info_box_element) > 4 else info_box_element[3].find('span', class_='black').text.strip()


            try:# Find the skills box
                skills_box_element = job_soup.find('ul', class_='c-infoBox u-mB0')
                skills_li_element = skills_box_element.find('h4', text='مهارت‌های مورد نیاز').parent if skills_box_element else ''
                # Get all the skill tags with class "black" within the skills box
                skill_tags = skills_li_element.find_all('span', class_='black') if skills_li_element else ''
                # Extract the skills and join them with a comma
                skills = ', '.join(skill_tag.text.strip() for skill_tag in skill_tags)
            except Exception as E:
                print(E)
                skills = ''
            # Find the gender box
            try:
                gender_li_element = skills_box_element.find('h4', text='جنسیت').parent
                gender = gender_li_element.find('span', class_='black').text.strip()
            except AttributeError:
                gender = ''

            # Find the military service box (is None when gender is set to 'female')
            try:
                military_service_li_element = skills_box_element.find('h4', text='وضعیت نظام وظیفه').parent
                military_service = military_service_li_element.find('span', class_='black').text.strip()
            except AttributeError:
                military_service = ''

            # Find the education box
            try:
                education_li_element = skills_box_element.find('h4', text='حداقل مدرک تحصیلی').parent
                education = education_li_element.find('span', class_='black').text.strip()
            except AttributeError:
                education = ''

            # Find the job description
            job_description_element = job_soup.find('div', class_='o-box__text s-jobDesc c-pr40p')
            job_description = job_description_element.get_text(strip=True) if job_description_element else ''

            # Append the job data to the list
            job_data_list.append({
                'Job Position': job_position,
                'Job Category': job_category,
                'Job Location': job_location,
                'Employment Type': job_employment_type,
                'Experience': job_experience,
                'Salary': job_salary,
                'Company Name': company_name,
                'Company Category': company_category,
                'Company Size': company_size,
                'Company Website': company_website,
                'Skills': skills,
                'Gender': gender,
                'Military Service': military_service,
                'Education': education,
                'Job Description': job_description,
                'Job URL': job_url
            })


async def main():
    async with aiohttp.ClientSession() as session:
        page_number = 1
        print(f"Processing page: {page_number} - Entry: 1")
        while True:
            url = initial_url + f'&page={page_number}'
            page_content = await fetch_page(session, url)
            if not page_content:
                break  # Stop crawling if the page is not accessible or doesn't exist

            soup = BeautifulSoup(page_content, 'html.parser')
            job_links = soup.find_all('a', class_='c-jobListView__titleLink')

            if not job_links:
                break  # Stop crawling if there are no job links on the page

            tasks = []
            entry_number = 1
            for job_link in job_links:
                print(f"Processing page: {page_number} - Entry: {entry_number}")
                tasks.append(process_job_page(session, job_link))
                entry_number += 1

            await asyncio.gather(*tasks)

            # Increment page number for the next iteration
            page_number += 1


# Run the event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



# Create a DataFrame from the collected job data list
df = pd.DataFrame(job_data_list)
df.to_csv('Jobinja - Async.csv', index=False, encoding='utf-8-sig')
print(df)