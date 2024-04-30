import streamlit as st
import openai

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can change the model as needed
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,  # Adjust the token limit as needed
        temperature=0.5  # Control creativity
    )
    return response.choices[0].message["content"].strip()

# Define the functions
def complete_code(partial_code):
    prompt = f"""
    Given the following partial Python code, complete it to make it a valid Python program:

    {partial_code}

    Return the completed code as a string.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


# Debugging assistance function
def debug_code(error_message):
    prompt = f"Suggest a fix for this error message:\n{error_message}"
    return ask_gpt(prompt)

# Documentation retrieval function
def documentation(query):
    prompt = f"Provide a Example and documentation for:\n{query}"
    return ask_gpt(prompt)

def main():
    # Define the application title and header
    #st.title("Smart Code Solutions")
    html_temp = """
    <div style="background-color:navy;padding:10px">
    <h2 style="color:white;text-align:center;">Smart Code Solutions </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    st.header("What would you like to do?")

    # Using columns for a more structured layout
    col1, col2 = st.columns(2)
    
    # Select box on the left column
    with col1:
        selected_option = st.selectbox("Select an option", ("Complete code", "Debug code", "Documentation"))
    
    # Text input on the right column
    with col2:
        text_input = st.text_area("Please enter any additional information or instructions")
    
    # Display the user's selection
    st.write("You selected:", selected_option)


    # Add a submit button
    if st.button("Submit"):
        # Access the function based on the selected option
        if selected_option == "Complete code":
            output = complete_code(text_input)
            st.code(output, language='python')
        elif selected_option == "Debug code":
            output = debug_code(text_input)
            st.write("Output:", output)
        elif selected_option == "Documentation":
            output = documentation(text_input)
            # Print the output from the function
            st.write("Output:", output)
    st.markdown("---")
    st.markdown("**Smart Code Solutions** is a project by Harsh.")         
        

# Run the main function
if __name__ == "__main__":
    main()
