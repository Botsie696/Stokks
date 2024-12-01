import openai
from youtube_transcript_api import YouTubeTranscriptApi
import sites
import json
import ast
import re
import financedata
import os
import videoFetcher
def safe_convert(value):
    try:
        return float(value)  # Try to convert to float
    except ValueError:
        return 0.0  # Return None if conversion fail

# Replace with your OpenAI API key
# 
openai.api_key = os.getenv("OPENAI_API_KEY")


def clean_and_extract(data):
    # Remove unwanted characters like ` and '
    clean_data = re.sub(r"[`']", "", data)

    # Extract the array content
    if clean_data.startswith("[") and clean_data.endswith("]"):
        clean_data = clean_data[1:-1]

    # Split into a list
    return [item.strip() for item in clean_data.split(",")]
def get_youtube_transcripts(video_url):
    try:
        # Extract video ID from the URL
        video_id = video_url.split("v=")[-1]
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine transcript segments into a single string
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None
import requests



def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error communicating with ChatGPT: {e}")
        return None
Transcripts = []
MajorTranscript = []
import math

def main(link):
    video_url = link  # Replace with your YouTube video URL
    
    transcript = videoFetcher.get_youtube_transcriptOnce(video_url)  # Fetch the YouTube transcript
    MajorTranscript.append(transcript)
    
    if not transcript:
        print("Failed to retrieve transcript. " + str(link) + str(transcript))
        return

    # Define token limit
    token_limit = 16385

    # Function to split transcript into chunks
    def split_transcript(transcript, chunk_size):
        words = transcript.split()  # Split transcript into words
        return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    # Estimate chunk size (adjust as needed based on average token size)
    avg_token_size = 4  # Average token size per word
    chunk_size = token_limit // avg_token_size

    # Split the transcript into manageable chunks
    transcript_chunks = split_transcript(transcript, chunk_size)
    # print(f"Transcript split into {len(transcript_chunks)} chunks.")

    # Process each chunk and accumulate recommendations
    full_recommendations = ""
    for index, chunk in enumerate(transcript_chunks, start=1):
        # print(f"Processing chunk {index}/{len(transcript_chunks)}...")
        prompt = (
            "Based on the following transcript, identify all stock recommendations mentioned "
            "(Give stock names and stock symbols with max 12-word descriptions each, prices if mentioned. "
            "Make bullet points for all stocks, explaining why each stock is selected and why it will rise):\n\n"
            f"{chunk}"
        )
        recommendations = ask_chatgpt(prompt)
        if recommendations:
            full_recommendations += recommendations + "\n"
        else:
            print(f"Failed to retrieve recommendations for chunk {index}.")

    if full_recommendations:
        Transcripts.append(full_recommendations)
        print("Recommendations successfully compiled.")
    else:
        print("Failed to retrieve any recommendations from ChatGPT.")

def analyze_recommendations(recommendations_list, trend):
    def chunk_text(text, max_length):
        """
        Splits a text into chunks with a maximum length.
        """
        chunks = []
        while len(text) > max_length:
            split_index = text[:max_length].rfind("+++")
            if split_index == -1:  # If no delimiter is found, split at max_length
                split_index = max_length
            chunks.append(text[:split_index])
            text = text[split_index:].lstrip("+++")  # Remove the delimiter at the start
        chunks.append(text)
        return chunks

    try:
        # Convert recommendations list into a single string
        recommendations_text = "+++ ".join(recommendations_list)
        # Set the maximum token length for the chunks
        max_tokens = 16000
        
        # Chunk the recommendations text if it exceeds the max length
        if len(recommendations_text) > max_tokens:
            chunks = chunk_text(recommendations_text, max_tokens)
        else:
            chunks = [recommendations_text]
        
        responses = []
        for chunk in chunks:
            prompt = (
                trend + "{" + f"{chunk}" + "}" +
                "keep everything short and less than 40 words  (each transcript is separated by '+++')'\n'"
            )
            response = ask_chatgpt(prompt)
            if response:
                responses.append(response)
            else:
                print("Failed to analyze stock recommendations with ChatGPT for a chunk.")
        
        # Combine responses from all chunks
        final_response = " ".join(responses)
        # print(final_response)
        return final_response

    except Exception as e:
        print(f"Error analyzing recommendations: {e}")
        return ""


def convertTo(recommendations_list, trend):
    try:
        prompt = (
            trend  + f"{recommendations_list}"
        )
        response = ask_chatgpt(prompt)
        if response:
            # print("Most Common Stock Recommendations:")
            # print(response)
            return response
        else:
            print("Failed to analyze stock recommendations with ChatGPT.")
    except Exception as e:
        print(f"Error analyzing recommendations: {e}")
# Common stocks
stocksAnalysis1 = "Based on the following list of stock recommendations, identify the most common stocks mentioned and top 10-12 stocks in total  and give only stock names and price if mentioned and make sure to mention how many times it has been mentioned overall from all transcripts:\n\n"
# Stocks to invest in from common 
Confident = "Based on the following list, which stock had a hard on recommendations, which transcript or transcripts were really confident to buy this one stock "
# News 
StockRose = "Which stock risen up the most of these transcripts, give only top 10 stocks that you feel according to transcripts rose the most, only stock names and why "
# some

StockRose = "Which stocks is a rise for couple of months, and has growth and will grow"
Which = "According to you what stocks should I buy on which stocks might go really high from these transcripts, only stock names "
# some
TORise= "Name all the stocks mentioned in these stocks, stock name and its symbol"

 

# ParticularStock = "Why is Crocs and Nike mentioned and why is it a BUY according to these transcripts"

AllRecommendations = [stocksAnalysis1 , Confident , StockRose , Which , TORise ]
# MAIN
stock_symbols = []
if __name__ == "__main__":
    with open("recommendations_output.txt", "w") as output_file:
        for n in sites.MainStokksArray:
            main(n)
        
        string_recommendations = "+++".join(Transcripts)
        
        AllResults = ""
        AllData = []
        for n in AllRecommendations:
            result = analyze_recommendations(string_recommendations , n)
            output_file.write(n + "\n" + result + "\n\n")
            
            data = convertTo((result), "Convert all stocks mentioned in this transcript to Stock symbols (They could be in brackets too like (TSLA) or maybe just mentioned), example Nasdaq to being NDAQ and add that to an ARRAY ONLY, if stock symbol is not mentioned just give entire stock name,o, FORMAT SHOULD BE THIS WAY ONLY, no other texts,  this format only give one array , Make sure to get all the stocks mentioned in these transcript, double check on them, give data like:  [NDAQ,APPLE,x,Y,Z]")
            stock_symbols = clean_and_extract(data)
            AllData = AllData + stock_symbols
        # Collect the strings from each analysis and write them to the file

        

        # data = convertTo((AllResults), "Convert all stocks mentioned in this transcript to Stock symbols (They could be in brackets too like (TSLA) or maybe just mentioned), example Nasdaq to being NDAQ and add that to an ARRAY ONLY, if stock symbol is not mentioned just give entire stock name,o, FORMAT SHOULD BE THIS WAY ONLY, no other texts,  this format only give one array , Make sure to get all the stocks mentioned in these transcript, double check on them, give data like:  [NDAQ,APPLE,x,Y,Z]")
        # output_file.write(data + "\n\n")
        # print("==" + data + "====")
        
        AllData = list(set(AllData))
         
        stock_symbols = AllData
        # print(stock_symbols)
        Rise = {}

        StockPrice = {}
        StockRevenue = {}
        Consistency = {}
        AverageScore = {}
        MedianScore = {}
        ConsistencyScores = {}
        HighestMedianScore =0 
        HighestAverageScore = 0
        HighestConsistancyScore = 0
        HighestRiseScore = 0
        
        for n in stock_symbols:
            # print("Printing data for " + n)
            Percent, Price  , Name = financedata.AnalyseWithYahoo(n)
            StockRev = financedata.GetRevenue(Name)
            ConsisStockRev , Average , Median , ScoresMids = financedata.ConsistancyScore(Name , 7)
            Rise[n] = str(Percent)
            Consistency[n] = ConsisStockRev
            ConsistencyScores[n] = ScoresMids
            AverageScore[n] = Average
            MedianScore[n] = Median
            StockPrice[n] = Price
            StockRevenue[n] = StockRev 
            

            if safe_convert(ScoresMids) > HighestConsistancyScore:
                HighestConsistancyScore = ScoresMids
            if safe_convert(Average)> HighestAverageScore:
                HighestAverageScore = Average
            if safe_convert(Median) > HighestMedianScore:
                HighestMedianScore = Median
             
            if safe_convert(Percent) > HighestRiseScore:
                HighestRiseScore = Percent
            

        for key, value in Rise.items():
            print(f"{key}: {value}")
        # print(Rise)

        file_path = "stocks.txt"

        # Filter and convert values to numbers
        filtered_dict = {k: safe_convert(v) for k, v in Rise.items() if safe_convert(v) is not None}

        # Sort the dictionary by value
        sorted_dict = dict(sorted(filtered_dict.items(), key=lambda item: item[1]))

        # Write to a text file
        file_path = "sorted_dictionary_output.txt"
        # print("Dicted")
        # print(sorted_dict)
        print("Writing to File")
        with open(file_path, "w") as file:
            for key, value in sorted_dict.items():
               ScoresPuts =0
               try:
                    print(MedianScore)
                    print(key)
                    Meds = (MedianScore[key] / HighestMedianScore)
                    Avgs = (AverageScore[key] / HighestAverageScore)
                    vals = (value / HighestRiseScore)
                    consis = (ConsistencyScores[key] / HighestConsistancyScore)
                    
                    ScoresPuts = round((Meds + Avgs + vals + consis) , 2)
               except TypeError:
                   pass
                   
               
               
               file.write(
                    f"{key},{value},{StockPrice[key]},{StockRevenue[key]},"
                    f"{Consistency[key]},{AverageScore[key]},{MedianScore[key]},{ScoresPuts}\n"
                    )
        import read
               
