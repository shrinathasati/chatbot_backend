from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

app = Flask(__name__)

# Define patterns and responses for the chatbot (your existing patterns)
patterns = [
    # Your chatbot patterns here...
    (r'hi|hello|hey', ['Hello! I am a chatbot made by Techgeeks']),
    (r'(.*) (depressed|anxious|lonely|loneliness|stressed|sad|irritate)',
        ['I’m sorry to hear that. Its okay to feel that way sometimes. How can I support you?']),
    (r'(.*) (need someone to talk to|mental health professional|nearby mental care center)',
        ['I am here to listen and offer support. What is been bothering you?']),
    (r'(.*) help with (.*)',
        ['I can provide information and suggestions. What do you need help with?']),
    # (r'(.*) (symptom of mental health|sign of mental health)', ['It is estimated that mental illness affects 1 in 5 adults in America, and that 1 in 24 adults have a serious mental illness. Mental illness does not discriminate; it can affect anyone, regardless of gender, age, income, social status, ethnicity, religion, sexual orientation, or background. Although mental illness can affect anyone, certain conditions may be more common in different populations. For instance, eating disorders tend to occur more often in females, while disorders such as attention deficit/hyperactivity disorder is more prevalent in children. Additionally, all ages are susceptible, but the young and the old are especially vulnerable. Mental illnesses usually strike individuals in the prime of their lives, with 75 percent of mental health conditions developing by the age of 24. This makes identification and treatment of mental disorders particularly difficult, because the normal personality and behavioral changes of adolescence may mask symptoms of a mental health condition. Parents and caretakers should be aware of this fact, and take notice of changes in their childâ€™s mood, personality, personal habits, and social withdrawal. When these occur in children under 18, they are referred to as serious emotional disturbances (SEDs).']),
    (r'(.*) (symptom of mental health|sign of mental health)', ['Common mental health signs and symptoms include changes in mood, behavior, and thoughts, along with physical and emotional symptoms. These indicators can vary depending on the specific mental health condition and its severity, making professional evaluation and support essential for diagnosis and treatment.']),
    (r'(.*) (mental health|mental illeness)', ['Mental health is feeling good and coping well with life, while mental illness is when you are struggling with your thoughts and emotions']),
    (r'(.*) (mental illness recover|recover)', ['Yes, many individuals with mental illnesses can recover, manage their conditions effectively, and lead fulfilling lives with the right treatment, support, and coping strategies. Recovery is possible and varies from person to person.']),
    (r'(.*) (help)', ['I will be very happy to help you']),
    (r'(.*) (dissociative indentity disorder)', ['Dissociative Identity Disorder (DID) is a rare mental health condition characterized by the presence of multiple distinct identities or personality states within one individual, often arising from a history of severe trauma. Treatment typically involves therapy to integrate these identities and address underlying trauma. ']),
    (r'(.*) (treatement for dissociative indentity disorder)', ['The primary treatment for DID involves psychotherapy, utilizing approaches such as Dialectical Behavior Therapy (DBT), Cognitive-Behavioral Therapy (CBT), or Eye Movement Desensitization and Reprocessing (EMDR) to address the unique challenges presented by different identity states. This treatment also emphasizes stabilization, helping individuals manage their symptoms, emotional regulation, and safety. Trauma-informed care is central to this process, recognizing and addressing past traumatic experiences. Additionally, support from loved ones and a respectful approach to the individuals autonomy are key. The ultimate goal is to work towards integration, merging the identity states into a more unified sense of self, although this is done in a manner that respects the individuals choices and progress. Its important to note that DID treatment is often a long-term endeavor, and ongoing support is crucial to successful management of the disorder.']),
    (r'(.*) (difference between mental health and mental illness)', ['Mental health relates to overall emotional well-being and the ability to cope with lifes challenges, while mental illness specifically refers to diagnosed conditions that disrupt a person mental and emotional functioning, often requiring treatment and support. Mental health encompasses a broad spectrum, while mental illness is a specific subset of mental health concerns.']),
    (r'(.*) (sucide)', ['Sucide is not a right way to solve any problem so please do not follow it']),
    (r'(.*) (income assistance|fee|pay)', ['There are so many goverment schemes for treatment and government treatement center you can visit which are affordabel']),
    # (r'(.*) ()', ['I will be very happy to help you']),
    (r'(.*) (help)', ['I will be very happy to help you']),
    (r'(.*) (help)', ['I will be very happy to help you']),

    (r'(.*) (medication)', ['Medication in mental health is essential for managing symptoms, restoring brain chemical balance, and improving the quality of life for individuals with various mental health conditions when used as part of a comprehensive treatment plan.']),
    (r'(.*) (physical health)', ['To care for your physical health, eat well, stay active, get enough rest, and avoid harmful habits like smoking and excessive drinking. Regular check-ups and staying safe can help keep you healthy.']),
    (r'(.*) (counsellor|psychaiatrist|psychologist)', ['I am currently working on that I will update the information soon']),
    (r'(.*) (CBT|DBT)', ['CBT (Cognitive Behavioral Therapy) focuses on changing negative thought patterns and behaviors, while DBT (Dialectical Behavior Therapy) specializes in managing intense emotions and improving relationships, often used for borderline personality disorder.']),
    (r'(.*) (addiction)', ['Sometimes addiction is harmful so please take care']),
    (r'(.*) (alcohol|drinking|durg|durgs|smoking)', ['this will harmful for your body and will affect your body system so please overcome pro']),
    (r'(.*) (ADHD)', ['ADHD stands for Attention-Deficit/Hyperactivity Disorder. It is a neurodevelopmental disorder that affects both children and adults.']),
    (r'(.*) (Prodrome)', ['A prodrome is an early or initial set of signs and symptoms that precede the full onset of a medical condition or disease. In the context of mental health, it can refer to the early warning signs or symptoms that precede a more acute phase of a mental health disorder. ']),
    (r'(.*) (trust|trust anyone)',['Trust is an expensive emotion not everyone can earn it.']),
    (r'(.*) (insomia|sleep|not rest)',['Insomnia is a common sleep disorder characterized by difficulty falling asleep, staying asleep, or experiencing poor-quality sleep, despite having the opportunity for sufficient sleep. ']),

    (r'(.*) (treatment of insomia|insommia treatment|sleep treatment|treatment of sleep  |not rest treatment| treatment of not rest)',['Establish a Consistent Sleep Schedule: Setting a consistent sleep routine is fundamental. Try going to bed and waking up at the same time every day, even on weekends. This routine helps regulate your body internal clock, making it easier to fall asleep and wake up naturally.Create a Relaxing Bedtime Routine: Prior to bedtime, engage in calming activities that signal your body to wind down. Reading a book, taking a warm bath, or practicing relaxation exercises can help prepare your mind and body for sleep. Steer clear of stimulating activities such as watching TV or using electronic devices, as these can disrupt the transition into sleep.Optimize Your Sleep Environment: Design your bedroom to be a sleep-friendly environment. Keep the room dark, quiet, and at a comfortable temperature. Investing in a comfortable mattress and pillows can significantly impact your sleep quality.Mindfulness and Stress Reduction: Incorporate relaxation techniques into your evening routine. Methods such as meditation, deep breathing exercises, or mindfulness practices can reduce stress and anxiety, making it easier to relax before bedtime.Regular Exercise: Engaging in regular physical activity during the day can promote better sleep. However, avoid exercising too close to bedtime, as it can have a stimulating effect that may interfere with falling asleep.Limit Stimulants and Screen Time: Cut back on stimulants like caffeine and nicotine close to bedtime, as they can hinder your ability to sleep. Additionally, reduce screen time an hour before bed as the blue light emitted by screens can disrupt the production of the sleep-inducing hormone melatonin.Consult a Healthcare Professional: If insomnia persists and significantly impacts your daily life, seek advice from a healthcare professional or sleep specialist. They can identify underlying causes and suggest suitable treatments, which might include therapy, medication, or cognitive-behavioral techniques aimed at improving sleep quality.Evaluate Your Diet: Assess your diet to avoid heavy meals and excessive liquids close to bedtime. Certain foods and drinks, like herbal teas or foods rich in tryptophan, may aid in promoting sleep.Remember, the effectiveness of these strategies may vary for each individual. Its crucial to find a personalized approach that works best for you. Seeking professional advice and making healthy lifestyle adjustments can greatly assist in managing insomnia. ']),
    (r'(.*)',['Sorry i can not understand please describe in proper way'])
    
]

# Create the chatbot
chatbot = Chat(patterns, reflections)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route to handle user input and get responses
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = chatbot.respond(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
