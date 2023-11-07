import string

def analyze_reviews(reviews):
    total_rating = 0  # Initialize total_rating as an integer
    word_count = {}
    monthly_reviews = {}
    STOPWORDS = set(["the", "and", "a", "to", "of", "in", "but", "some", "is", "it", "for", "on", "with", "was"])

    for review in reviews:
        # Task 1: Calculate the average rating
        total_rating += int(review["rating"])  # Convert the rating to an integer

        # Task 2: Identify the most common words
        review_text = review["review"].lower()  # Convert to lowercase
        # Split the review text into words and remove punctuation
        words = [''.join(char for char in word if char not in string.punctuation) for word in review_text.split()]
        for word in words:
            if word not in STOPWORDS and word:  # Ensure the word is not in STOPWORDS and is not empty
                word_count[word] = word_count.get(word, 0) + 1

        # Task 3: Find the month with the most reviews submitted
        month = review["date"].split("-")[1]
        monthly_reviews[month] = monthly_reviews.get(month, 0) + 1

    # Calculate the average rating as a float
    average_rating = total_rating / len(reviews)

    max_word_count = max(word_count.values())
    most_common_words = sorted([word for word, count in word_count.items() if count == max_word_count])

    month_name = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }

    most_reviews_month = month_name[max(monthly_reviews, key=monthly_reviews.get)]

    print(f"Average Rating: {average_rating:.1f}")  # Format as a float with one decimal place
    print(f"Most Common Words: {most_common_words}")
    print(f"Month with Most Reviews: {most_reviews_month}")

reviews = [
    {"id": 1, "rating": 5, "review": "The coffee was fantastic.", "date": "2022-05-01"},
    {"id": 2, "rating": 4, "review": "Excellent atmosphere. Love the modern design!", "date": "2022-05-10"},
    {"id": 3, "rating": 3, "review": "The menu was limited.", "date": "2022-05-20"},
    {"id": 4, "rating": 4, "review": "Highly recommend the caramel latte.", "date": "2022-05-22"},
    {"id": 5, "rating": 4, "review": "The seating outside is a nice touch.", "date": "2022-06-01"},
    {"id": 6, "rating": 5, "review": "It's my go-to coffee place!", "date": "2022-06-07"},
    {"id": 7, "rating": 3, "review": "I found the Wi-Fi to be quite slow.", "date": "2022-06-10"},
    {"id": 8, "rating": 4, "review": "Menu could use more vegan options.", "date": "2022-06-15"},
    {"id": 9, "rating": 4, "review": "Service was slow but the coffee was worth the wait.", "date": "2022-06-28"},
    {"id": 10, "rating": 2, "review": "Very noisy during the weekends.", "date": "2022-07-05"},
    {"id": 11, "rating": 5, "review": "Baristas are friendly and skilled.", "date": "2022-07-12"},
    {"id": 12, "rating": 3, "review": "It's a bit pricier than other places in the area.", "date": "2022-07-20"},
    {"id": 13, "rating": 4, "review": "Love their rewards program.", "date": "2022-07-25"},
]

analyze_reviews(reviews)
