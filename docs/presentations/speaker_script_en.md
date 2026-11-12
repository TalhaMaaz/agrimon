---
type: presentation
status: final
tags: [presentation, mid-semester, script]
phase: R
---

# AgriMon mid-semester presentation: full English script

Written from the deck's speaker notes (deck version 433) and the text on each slide. About 1,800 words: roughly 12 to 13 minutes at a calm pace, so it is longer than the 10-minute slot. Words in [square brackets] are choices you still have to make.

## Slide 1: Cover

Assalam o Alaikum, everyone. My name is Muhammad Talha Maaz, and my project is "Satellite and AI-Based Crop Monitoring and Decision-Support System for Sugarcane". It is supervised by Dr. Aneela Zameer.

This is an academic prototype. It is inspired by a real problem my startup faces, but I am building it only on open data.

## Slide 2: Background and motivation

Sugarcane matters a great deal to Pakistan. It is grown on more than 3 million acres, the country produces about 89 million tonnes a year, and sugar is Pakistan's second-largest agro-based industry.

I chose this project because I am linked with an agritech startup. Thirty-three sugar mills in Pakistan are on our waiting list, and we have already given prototype systems to some of them. Our major client and investor is JDW Corporate Farms. We have digitised 4.5 lakh acres of their land, that is 450,000 acres, and their agronomists use our product to monitor their fields.

What I am presenting today, though, is an academic prototype built on open data.

## Slide 3: Problem statement

From talking to Pakistani sugar mills, we learned that most of them still monitor their crop through manual field surveys. Their agents go field by field with a GPS app. Satellite-based, per-field monitoring does not exist for them.

This matters because every year, before the crushing season, a mill has to estimate how much cane its farmers will supply. It plans procurement and sets its price from that estimate. My project aims to help mill leadership make those decisions by monitoring their sugarcane fields from satellite data.

Open data does not answer the mill's questions today. A recent sugarcane map covering 13 countries had a recall of only 43 % in Pakistan: it found less than half of the real cane, because there is no local labelled data here.

My supervisor put me in touch with SUPARCO. SUPARCO is the main national body for satellite-based crop monitoring and yield forecasting, but its job is to support the government's statistics departments, not individual mills.

## Slide 4: Aim, objectives and scope

My aim is a web portal where digitised fields appear on a map, each with a label for which crop is growing and a history of its health.

There are five objectives: a pipeline that turns open data into a time series for each field; a crop-type model that separates cane from non-cane and is tested on years and areas it has never seen; a health layer; an indicative yield; and a web map that brings all of this together.

For health: a satellite measures crop vigour, in other words greenness. I compare each field with the normal sugarcane growth cycle to infer its health. So I will not diagnose pests or diseases, but I can show their effects and flag them.

For yield: I will build a regression model on past official yields and vegetation indices such as NDVI. I will show an indicative yield for every field, but I cannot validate it at field level, because there is no field-level ground truth. According to my company's domain expert, that needs the most important variables measured on the ground, which I cannot do yet. I plan to start that work after my degree.

The non-functional requirements are: the system must be easy for non-professionals such as a mill officer to use, with plain labels and a clear legend; the whole pipeline must run on modest hardware, meaning my laptop or free Colab and Kaggle; and the map must stay smooth with around 5,600 fields in one parish.

## Slide 5: The interface we will build

This is what the final interface will look like. It brings together the tools an agronomist needs to monitor their fields. You click a field and see its crop, its health and its yield. There is also a date slider, so the user can look back at the analysis of older satellite images.

Please note this is a mockup, not real results. The field shapes on the map are real fields from Iberia parish in Louisiana, coloured by their 2023 crop.

## Slide 6: Existing systems

Now, what already exists. In Pakistan, SUPARCO does crop monitoring, but its work is statistics for the government, and its yield models use coarse 1-kilometre NDVI. There is no tool for sugar mills.

Commercial platforms such as Cropin and OneSoil do offer crop monitoring, but they are closed source and are not tailored to Pakistan's agriculture.

## Slide 7: What research shows

What did the research show? An international study mapped sugarcane in 13 countries, but in Pakistan its recall was only 43 %, because there were no local labels.

A local study in Punjab got good results with deep learning, but only on about 130 acres of labelled cane. I have asked its authors for the dataset.

Another study predicted sugarcane yield from satellite and weather data, using the same US data sources I use. And studies from France showed that deep models built for time series beat Random Forest, and that feeding the model one record per field works.

Finally, crop-health work defines health as departure from normal, which I apply per field. My system uses these findings to build three modules, and joins them into one complete decision-support system.

## Slide 8: Proposed solution and methodology

The open datasets my FYP needs do not exist in Pakistan. In particular, there is no practical dataset with field boundaries, which this application depends on. The US has one.

So the method has two stages. In Stage 1, now, I build and prove the system on available data from the US. In Stage 2, at the end of the FYP, I adapt it to Pakistan. I have contacted [SUPARCO and NUST / SUPARCO and the authors of the Punjab study] for field boundaries. If that data is not available, I will adapt the models to Pakistani conditions and draw the field boundaries from satellite images.

My company has digitised about 8 lakh acres from the ground, including JDW's 4.5 lakh. But this project is about open data, and because of company policy I am not using that data in my FYP.

The work is iterative, in an Agile style: plan, approve, build, review.

## Slide 9: Datasets selected

Here are the datasets. Field boundaries come from the USDA Crop Sequence Boundaries, about 206,000 fields in Louisiana. Crop labels come from the USDA Cropland Data Layer. For sugarcane in Louisiana it has about 95 % producer's accuracy and 96 % user's accuracy, meaning it finds 95 % of the cane and is right 96 % of the time when it says cane. Images come from Sentinel-2, and official yields come from USDA NASS.

The biggest reason for this choice is 18 seasons of sugarcane data, from 2008 to 2025. That lets me do a temporal hold-out: train on some years and test on years the model has never seen. It also lets me learn what a normal cane season looks like, which the health layer needs.

I also looked at La Réunion, Brazil and EuroCrops, but each was missing something essential: field polygons, sugarcane, recent fields or enough seasons.

## Slide 10: System architecture

First, the system collects data from every source: satellite imagery, field boundaries with crop labels, and yield and weather data. The ingestion layer gives every source one common interface. This is the adapter pattern, so any source can be swapped out later, for example for Pakistani data.

All the data is brought into one common coordinate reference system, and each field gets its own time series. The single unit of my data is a field; I do not store whole satellite images.

Three models then run on this per-field data: crop type, health and yield. The results appear on a web map, with layers, a date slider and a field pop-up.

## Slide 11: Use-case diagram

The use-case diagram has two main users. The mill officer or agronomist views the map, clicks on a field to see its crop type, health history and indicative yield, and can change the date.

The developer runs the pipeline, evaluates the models, and pulls in data for new fields or regions to ingest into the system.

## Slide 12: Database design

In the database design, everything is linked to FIELD. Each field has crop labels year by year, satellite index observations, and predictions.

FIELD and REGION have a one-to-many relationship: one region contains many fields, and each region has its official yield statistics.

## Slide 13: Technologies and tools

The stack is open and free. I use Python's geospatial libraries, Sentinel-2 images from Planetary Computer, and GeoParquet and DuckDB for storage.

GeoParquet is a column-based geospatial file format. In my files each row is one field, with its shape and its values. It is compressed and fast, and it needs no server. DuckDB is an embedded, in-process analytical database: it runs inside Python and can run SQL queries directly on these files.

The models start with a Random Forest baseline, then move to TempCNN and attention models in PyTorch. The frontend will be built on MapLibre.

Satellite data can also be fetched through the Earth Engine API, but that is optional, because its free tier is for noncommercial work only.

## Slide 14: Initial progress

Before building any model, I checked whether the data is good enough, and I set the acceptance criteria for every check in advance.

The checks passed. Louisiana has 206,389 field polygons. Iberia parish alone had 4,213 cane fields in 2023, against a minimum of 1,000. The median cane field is 11.5 acres, about 465 Sentinel-2 pixels. And a typical cane field is 94.9 % cane pixels, against a requirement of at least 90 %.

The project environment, the research agent setup, the first round of the literature review, dataset selection and data exploration are complete. Dataset preprocessing is in progress now.

## Slide 15: Timeline and future plan

In Semester 7, the environment, data selection, and validation of the fields and labels are done. Still left this semester: validating the imagery and yield data, the second round of the literature review, and model selection. The architecture is final; the models will be chosen through experiments.

In Semester 8 come Modules A, B and C and the web map, then the Pakistan stage, the thesis and the defence.

Throughout this whole period, I am also taking courses in machine learning and geospatial software engineering.

## Slide 16: Thank you

Thank you very much. I am now happy to take your questions.

*For your preparation only, do not read aloud:* Why US data? The labels come from a model, so how do you know they are right? How is this different from SUPARCO and Cropin? What does "health" mean if you do not diagnose disease? Why no database server?
