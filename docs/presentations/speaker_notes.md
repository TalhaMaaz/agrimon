---
type: presentation
status: final
tags: [presentation, speaker-notes]
phase: R
---

# Mid-semester deck: speaker notes (Roman Urdu)

Exported from the deck on 2026-11-10 (version 373): https://claude.ai/artifact/N6e6SsWzupuPcMasPJ46eX. Printable cue cards: [cue_cards.html](cue_cards.html) (open in a browser, print A4 landscape, margins none).

## 1. cover

Assalam o Alaikum everyone, mera naam Muhammad Talha Maaz hai aur mera project “Satellite and AI-Based Crop Monitoring and Decision-Support System for Sugarcane” hai, jisko Dr. Aneela Zameer supervise kar rahi hain.

Yeh humare startup ke problem se inspired aik academic prototype hai, jo main sirf open data pe bana raha hoon.

## 2. background

Sugarcane Pakistan ke liye bohat aham hai: 3 million acres se zyada pe ugti hai, aur sugar Pakistan ki doosri sab se bari agro-based industry hai.

Is project ko maine is liye choose kiya kyunki main aik agritech startup ke sath linked hoon. Pakistan ki 33 sugar mills humari waiting list mein hain, aur kuch ko hum ne apne prototype systems provide bhi kar diye hain.

Humare major client aur major investor JDW Corporate Farms hain, jin ke 4.5 lakh (450,000) acres hum ne digitise kar liye hain, aur un ke agronomists humare product ko use kar ke apni field monitoring kar rahe hain.

Yeh aik open data pe based academic prototype hai.

## 3. problem

Pakistani sugar mills se humein pata laga ke zyada tar mills ki crop monitoring manual field surveys pe based hai; satellite-based per-field monitoring majood nahi. Har saal milling cycle se pehle sugar mills ne apni current farm yields ke hisab se farmers se sugarcane lene ki planning karni hoti hai aur apni price decide karni hoti hai.

Humara project companies ki leadership ko assist karega, taake woh apni sugarcane fields ko monitor kar ke milling cycle ke faislay le sakein.

13 mulkon wale sugarcane map ki Pakistan mein recall sirf 43% thi, yani asal cane ka sirf 43% detect hua, kyunki yahan local labelled data nahi.

SUPARCO se mujhe meri supervisor ne contact faraham kiya tha. Satellite-based government crop monitoring aur yield forecasting mein SUPARCO main idara hai, aur us ka kaam government ke statistical departments ko assist karna hai.

## 4. aim

Humara aim aik web portal banana hai, jis mein map pe digitized fields nazar aayengi, un ke labels honge ke kaunsi crop lagi hui hai, aur un ki health history kaisi hai. Pichle saalon ki official yields aur vegetation indices (jaise NDVI) pe regression model bana kar hum indicative yield estimate karenge.

Satellite crop vigour, yani greenness, measure karta hai, aur normal cane cycle se compare kar ke hum health infer karte hain; is liye hum kisi disease ya pest ki diagnosis nahi karenge, lekin kisi disease ke effects zaroor dekh kar inform kar sakte hain.

Har field ka indicative yield dikhayenge, lekin usay field level pe validate nahi kar sakte, kyunki field-level ground truth nahi hai. Company ke domain expert ke mutabiq is ke liye ground se sab se important variables ka data lena parega, jo abhi main nahi kar sakta; degree ke baad yeh kaam shuru karunga.

## 5. interface

Mere project ka final interface is tarah ka hoga, jis mein woh saare tools majood hain jo aik agronomist ko apni fields monitor karne ke liye zaroori hain. Is mein aik date slider bhi hoga, jis se purani satellite images ka analysis user ko dikhayenge. Yeh abhi aik mockup hai, asal results nahi.

## 6. existing

Ab dekhte hain ke abhi kya majood hai. Pakistan mein SUPARCO crop monitoring karta hai, lekin us ka kaam government ke liye statistics hai, aur us ke yield models 1 km NDVI use karte hain; sugar mills ke liye koi tool nahi.

Commercial platforms jaise Cropin aur OneSoil crop monitoring dete hain, lekin closed source hain aur Pakistan ki agriculture ke liye tailored nahi.

## 7. gap

Research se kya pata chala: aik international study ne 13 mulkon ka sugarcane map banaya, lekin Pakistan mein us ki recall sirf 43% thi, kyunki local labels nahi the. Punjab mein aik local study ne deep learning se achha result liya, lekin sirf 130 acres pe, jin se maine dataset ki request ki hai.

Aik aur study ne satellite aur weather data se yield predict ki, aur France ki studies ne dikhaya ke time-series deep models Random Forest se behtar hain.

Humara system in findings ko use kar ke 3 modules banayega, aur unko jod kar aik complete decision-support system.

## 8. method

Pakistan mein humari FYP ke liye zaroori open datasets majood nahi. Maine SUPARCO aur Punjab wali study ke authors se contact kiya hai, agar woh data provide kar dein.

Humari company ne ground se taqreeban 8 lakh acres digitise kiye hain (JDW ke 4.5 lakh samait), lekin is project ka focus open datasets hai, aur company ki policies ki wajah se main woh data FYP ke liye use nahi kar raha.

Kaam iterative hai, Agile style: plan, approve, build, review.

## 9. architecture

Sab se pehle system har source se data laata hai: satellite imagery, field boundaries aur crop labels, aur yield aur weather data. Ingestion layer sab sources ke liye aik common interface rakhti hai (adapter pattern), is liye koi bhi source baad mein badla ja sakta hai, jaise Pakistan ke data ke liye.

Saara data aik common CRS (coordinate reference system) mein aata hai aur har field ki aik time series banti hai. Humare data structure ki single unit aik field hai; poori satellite images store nahi karte.

Phir is per-field data pe teen models chalte hain: crop type, health aur yield. Results web map pe dikhte hain, layers, date slider aur field pop-up ke sath.

## 10. usecases

Use-case diagram mein do main users hain. Mill officer ya agronomist map dekhta hai, kisi field pe click kar ke crop type, health history aur indicative yield dekhta hai, aur date bhi change kar sakta hai.

Developer pipeline chalata hai, models evaluate karta hai, aur nayi fields ya regions ka data pull kar ke system mein ingest karta hai. Sentinel-2 aur doosre data sources external (secondary) actors hain.

## 11. datamodel

Database design mein har cheez FIELD se judi hai: har field ke saal-ba-saal crop labels, satellite index observations aur predictions.

FIELD aur REGION mein one-to-many relationship hai: aik region mein kai fields, aur har region ke official yield statistics hain.

## 12. stack

Stack open aur free hai: Python ki geospatial libraries, Planetary Computer se Sentinel-2 images, storage ke liye GeoParquet aur DuckDB.

GeoParquet aik column-based geospatial file format hai; humari files mein har row aik field hai, us ki shape aur values ke sath; compressed aur fast, server ki zaroorat nahi. DuckDB aik embedded (in-process) analytical database hai, jo Python ke andar chalta hai aur in files pe seedha SQL queries chala sakta hai.

Models LightGBM se shuru honge, phir TempCNN aur attention models PyTorch mein. Frontend MapLibre pe hoga.

Earth Engine API se bhi satellite data fetch kar sakte hain, lekin woh optional hai kyunki us ka free tier sirf noncommercial kaam ke liye hai.

## 13. datasets

Datasets: USDA CSB se field boundaries, CDL se crop labels, jis ki Louisiana mein cane ke liye taqreeban 95% producer's accuracy aur 96% user's accuracy hai, Sentinel-2 se images, aur NASS se official yields.

Sab se bari wajah 18 seasons ka sugarcane data hai, 2008 se 2025 tak, taake temporal hold-out kar sakein: kuch saalon pe train aur un saalon pe test jo model ne kabhi nahi dekhe.

La Réunion, Brazil aur EuroCrops bhi dekhe, lekin har ek mein koi zaroori cheez missing thi.

## 14. progress

Model banane se pehle maine check kiya ke data kaafi achha hai ya nahi, aur har check ke acceptance criteria pehle se set kiye.

Environment, requirements, literature review aur dataset selection mukammal hain; ab preprocessing chal rahi hai.

## 15. timeline

Semester 7 mein environment, data selection aur fields aur labels ki validation ho chuki hai. Is semester mein baqi: imagery aur yield data ki validation, literature ka doosra round aur model selection. Architecture final ho chuka hai; models experiments se chune jayenge.

Semester 8 mein Module A, B, C aur web map, phir Pakistan wala stage, thesis aur defence.

Is poore arsay mein main machine learning aur geospatial software engineering ke courses bhi kar raha hoon.

## 16. thanks

Bohat shukriya, ab main sawalat ke liye hazir hoon.

Tayyari ke liye: US data kyun? Labels model se hain to sahi kaise? SUPARCO aur Cropin se farq? Health ka matlab kya, agar disease diagnose nahi karte? Database server kyun nahi?
