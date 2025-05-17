from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
from tqdm import tqdm
import json
from selenium.webdriver.common.action_chains import ActionChains
import random
import urllib.parse

# Configuration
DECOY_LINKS = [
    "https://www.google.com",
    "https://www.edge",
    "https://www.spotify.com",
    "https://ktu.com",
    "https://www.abhilash.com"
]

# Configure Edge options
edge_options = Options()
temp_profile_dir = os.path.join(os.getcwd(), "temp_edge_profile")
os.makedirs(temp_profile_dir, exist_ok=True)

edge_options.add_argument(f"--user-data-dir={temp_profile_dir}")
edge_options.add_argument("--profile-directory=Default")
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-extensions")
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_experimental_option('useAutomationExtension', False)

# Initialize driver
driver = webdriver.Edge(options=edge_options)

def human_like_behavior():
    """Simulate human-like browsing behavior"""
    try:
        viewport_width = driver.execute_script("return window.innerWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        actions = ActionChains(driver)
        
        # Random mouse movements within safe bounds
        for _ in range(random.randint(2, 4)):
            x = random.randint(50, max(100, viewport_width - 100))
            y = random.randint(50, max(100, viewport_height - 100))
            actions.move_by_offset(x, y).pause(random.uniform(0.1, 0.5)).perform()
        
        # Random scrolling
        scrolls = random.randint(1, 3)
        for _ in range(scrolls):
            scroll_amount = random.randint(200, min(500, viewport_height//2))
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(0.3, 1.0))
            
    except Exception as e:
        print(f"Behavior simulation error: {str(e)}")

def visit_decoy_links():
    """Visit 1-3 random decoy links before the target URL"""
    num_decoys = random.randint(1, 3)
    decoys = random.sample(DECOY_LINKS, num_decoys)
    
    for decoy in decoys:
        try:
            print(f"Visiting decoy: {decoy}")
            driver.get(decoy)
            time.sleep(random.uniform(1.5, 3.5))  # Random wait time
            human_like_behavior()
            
            # Random chance to click on page elements
            if random.random() > 0.7:  # 30% chance to click something
                try:
                    clickable = driver.find_elements(By.CSS_SELECTOR, "a, button")[:10]
                    if clickable:
                        random.choice(clickable).click()
                        time.sleep(random.uniform(1.0, 2.5))
                        human_like_behavior()
                except:
                    pass
                    
        except Exception as e:
            print(f"Decoy visit error: {str(e)}")

def validate_url(url):
    """Ensure URLs are properly formatted"""
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme:
            url = "https://" + url
        return url.strip()
    except:
        return None

def scrape_article(url):
    """Scrape target article with human-like patterns"""
    result = {"url": url, "title": "", "date": "", "content": "", "error": None}
    
    try:
        # Visit decoy links first
        visit_decoy_links()
        
        # Now process target URL
        clean_url = validate_url(url)
        if not clean_url:
            result["error"] = "Invalid URL format"
            return result
            
        print(f"\nProcessing target: {clean_url}")
        driver.get(clean_url)
        
        # Human-like waiting pattern
        time.sleep(random.uniform(2.0, 4.5))
        human_like_behavior()
        
        # Wait for page to load
        try:
            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Additional random delay
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            result["error"] = f"Page load timeout: {str(e)}"
            return result
        
        # Get page source
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract content with multiple fallbacks
        title = (soup.find("h1") or 
                soup.find("title") or 
                soup.find("meta", {"property": "og:title"}))
        
        if title:
            result["title"] = title.get_text(" ", strip=True) if hasattr(title, 'get_text') else str(title)
        
        date = (soup.find("time") or
               soup.find("span", class_=lambda x: x and "date" in x.lower()) or
               soup.find(string=lambda t: t and any(w in t.lower() for w in ["published", "date", "updated"])))
        
        if date:
            result["date"] = date.get_text(" ", strip=True) if hasattr(date, 'get_text') else str(date)
        
        article = (soup.find("article") or
                  soup.find("div", class_=lambda x: x and "content" in x.lower()) or
                  soup.find("div", id=lambda x: x and "content" in x.lower()) or
                  soup.body)
        
        if article:
            paragraphs = []
            for p in article.find_all("p"):
                text = p.get_text(" ", strip=True)
                if text and len(text) > 20:
                    paragraphs.append(text)
            result["content"] = "\n\n".join(paragraphs)
        
        # Random post-reading behavior
        if random.random() > 0.5:  # 50% chance to scroll back up
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(random.uniform(0.5, 1.5))
        
        return result
        
    except Exception as e:
        result["error"] = f"Processing error: {str(e)}"
        return result

def process_links_file(input_file):
    """Process all links from input file"""
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return
        
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            links = [validate_url(link.strip()) for link in file if link.strip()]
            links = [link for link in links if link]  # Remove invalid URLs
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return
    
    results = {}
    
    for link in tqdm(links, desc="Processing Articles"):
        try:
            # Random delay between articles (3-8 seconds)
            time.sleep(random.uniform(3, 8))
            results[link] = scrape_article(link)
        except Exception as e:
            print(f"Fatal error processing {link}: {str(e)}")
            results[link] = {"url": link, "error": str(e)}
            
            # Try to recover the session
            try:
                driver.quit()
            except:
                pass
            driver = webdriver.Edge(options=edge_options)
    
    # Save results
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_results.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    try:
        input_file = 'Data/accepted_links/deshabhimani_accepted.txt'
        process_links_file(input_file)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        try:
            driver.quit()
        except:
            pass
        # Clean up temporary files
        try:
            import shutil
            shutil.rmtree(temp_profile_dir, ignore_errors=True)
        except:
            pass