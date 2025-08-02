import sans, dateparser, jinja2
from dataclasses import dataclass
from datetime import timezone

VERSION = "0.1.0"

@dataclass
class MostPosts:
    name: str
    posts: str

@dataclass
class MostLiked:
    name: str
    likes: str

nation = input("Main nation: ")

user_agent = sans.set_agent(f"rmbstats/{VERSION} by Merethin, used by {nation}")

print(f"Running with user agent '{user_agent}'.")
input(f"Press Enter to confirm.")

query = {}

while True:
    region = input("Region to check: ").lower().replace(" ", "_")

    start = input("Start date: ")
    end = input("End date: ")

    SETTINGS = {'DATE_ORDER': 'DMY', 'TIMEZONE': 'UTC', 'TO_TIMEZONE': 'UTC', 'PREFER_DAY_OF_MONTH': 'first'}

    start_time = dateparser.parse(start, settings=SETTINGS).replace(tzinfo=timezone.utc)
    end_time = dateparser.parse(end, settings=SETTINGS).replace(tzinfo=timezone.utc)

    if not start_time or not end_time:
        print("Invalid start or end date! Please try again.")
        continue

    print(f"Query settings: region={region}, from='{start_time.strftime("%d/%m/%Y, %H:%M:%S %:z")}', to='{end_time.strftime("%d/%m/%Y, %H:%M:%S %:z")}'")
    accept = input("Confirm query? [y/N] ")
    if accept.lower() == "y":
        query['region'] = region
        query['from'] = int(start_time.timestamp())
        query['to'] = int(end_time.timestamp())
        break

mostposts = []
mostliked = []
mostlikes = []

client = sans.Client()
query["q"] = "mostposts"
response = client.get(sans.API_URL.copy_with(params=query))

for element in response.xml.findall("./MOSTPOSTS/NATION"):
    nation = element.find("NAME").text
    if nation is None:
        continue

    posts = element.find("POSTS").text
    mostposts.append(MostPosts(nation, posts))

query["q"] = "mostliked"
response = client.get(sans.API_URL.copy_with(params=query))

for element in response.xml.findall("./MOSTLIKED/NATION"):
    nation = element.find("NAME").text
    if nation is None:
        continue

    liked = element.find("LIKED").text
    mostliked.append(MostLiked(nation, liked))

template_name = input("Query finished. Enter template name (in the templates folder): ")
top = input("Number of top entries (leave empty to show all): ")
if top != "":
    mostposts = mostposts[:int(top)]
    mostliked = mostliked[:int(top)]

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
template = env.get_template(template_name)
output = template.render(mostposts=mostposts, mostliked=mostliked)

file_name = input("Enter output file name: ")

with open(file_name, 'w') as f:
    print(output, file = f)