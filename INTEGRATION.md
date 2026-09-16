# Deni: channel integration (USSD and WhatsApp, sandbox)

Deni meets people on the channel they have. This guide sets up both extra channels in
their providers' **sandboxes**, enough for a live demo, with no telco shortcode or
business verification.

## What each channel does

Same civic engine, different reach:

- **Web** (`/app`): the full experience.
- **WhatsApp**: conversational near-full. Paste a loan SMS and get the true cost; type
  a lender's name and get its licence status and findings; describe a problem and get
  the law, the public body, and a prepared complaint.
- **USSD**: the essentials on any feature phone with no internet: true cost of listed
  products, lender licence check, and read your rights. (USSD is menu-only and short,
  so complaint generation and pasting live on WhatsApp/web, not USSD, by design.)

## Prerequisite: a public URL

Both providers POST to your app, so it must be reachable from the internet. For a demo,
run the app locally and tunnel it:

```bash
bash run.sh                 # starts Deni on http://127.0.0.1:8000
ngrok http 8000             # in another terminal; gives https://XXXX.ngrok.io
```

Use the `https://XXXX.ngrok.io` URL below. (Or deploy to Render/Railway/Fly and use
that URL instead.)

---

## USSD (Africa's Talking sandbox)

No API key and no code change: the `/ussd` endpoint already speaks the AT protocol.

1. Create a free account at africastalking.com and open the **Sandbox**.
2. Go to **USSD -> Create Channel**. You get a test code like `*384*<n>#`.
3. Set the channel's **callback URL** to:
   ```
   https://XXXX.ngrok.io/ussd
   ```
4. Open the AT **Simulator** (Sandbox -> Launch Simulator), enter a phone number, and
   dial your code.
5. Navigate the menu:
   - `1`/`2`/`3` -> a modelled product's true cost + licence line
   - `4` -> type a lender name -> licensed / not
   - `5` -> Know your rights -> pick a scenario -> the law + the public body

That is a real USSD session; AT posts each keypress to `/ussd` and shows your reply.

---

## WhatsApp (Twilio sandbox)

1. Create a free Twilio account at twilio.com.
2. Go to **Messaging -> Try it out -> Send a WhatsApp message** to open the WhatsApp
   sandbox. It shows a Twilio number and a join code like `join <word-word>`.
3. From your own WhatsApp, send `join <word-word>` to that number to opt in.
4. In the sandbox settings, set **"When a message comes in"** to:
   ```
   https://XXXX.ngrok.io/webhook/twilio
   ```
   method **POST**.
5. Message the sandbox number from your WhatsApp:
   - `hi` -> the menu
   - paste a loan SMS, or `1000, 1150, 30` -> the true cost (182.5% APR)
   - `Tala` after choosing `2`, or just a lender name -> licence status + findings
   - `they are calling my contacts` -> the law, the public body, and a prepared
     complaint you can edit and send

Twilio delivers the reply Deni returns (as TwiML) straight back to your WhatsApp.

### Notes

- `/webhook/twilio` accepts Twilio's form POST (`From`, `Body`) and returns TwiML.
- `/webhook/whatsapp` accepts JSON (`{sender, message, country}`) and is used by tests
  and by generic providers.
- Session state is in-memory (per sender), which is fine for a demo; production would
  use Redis or a database.
- Add `?country=za` to a webhook URL to serve the South Africa pack instead of Kenya.

## Honesty for the demo

These run in provider sandboxes: real behavior, no production shortcode or approved
WhatsApp Business number. Going live needs a paid USSD shortcode (telco approval, per
country) and WhatsApp Business verification. State this in the demo and deck.
