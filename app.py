# import pandas as pd
# from shiny import App, render, ui, reactive
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the data from the provided Excel file
# file_path = r'C:\Users\anas.kali\Desktop\Kariyer_Tasks\CommentsAutomation\Translated_Negative_Reviews.xlsx'
# data = pd.read_excel(file_path)

# # Define the mappings for categories and languages
# category_language_mapping = {
#     "User Interface Issues": {
#         "TR": "Kullanıcı Arayüzü Sorunları (TR)",
#         "EN": "User Interface Issues (EN)"
#     },
#     "Performance Problems": {
#         "TR": "Performans Sorunları (TR)",
#         "EN": "Performance Problems (EN)"
#     },
#     "Job Search Functionality": {
#         "TR": "İş Arama İşlevselliği (TR)",
#         "EN": "Job Search Functionality (EN)"
#     },
#     "Notification Issues": {
#         "TR": "Bildirim Sorunları (TR)",
#         "EN": "Notification Issues (EN)"
#     },
#     "Application Process": {
#         "TR": "Başvuru Süreci (TR)",
#         "EN": "Application Process (EN)"
#     },
#     "Profile Management": {
#         "TR": "Profil Yönetimi (TR)",
#         "EN": "Profile Management (EN)"
#     },
#     "Customer Support": {
#         "TR": "Müşteri Desteği (TR)",
#         "EN": "Customer Support (EN)"
#     },
#     "Account Management": {
#         "TR": "Hesap Yönetimi (TR)",
#         "EN": "Account Management (EN)"
#     }
# }

# # Flatten the mapping for easier access
# flattened_mapping = {v[lang]: k for k, v in category_language_mapping.items() for lang in v}

# # Prepare UI layout with visual enhancements
# app_ui = ui.page_fluid(
#     ui.h2("Negative Reviews Dashboard"),
#     ui.layout_sidebar(
#         ui.panel_sidebar(
#             ui.input_select("category", "Select Category", {k: k for k in category_language_mapping.keys()}),
#             ui.input_radio_buttons("language", "Select Language", {"TR": "Turkish", "EN": "English"}),
#             ui.input_text("keyword", "Keyword Search", ""),
#             ui.input_action_button("show_comments", "Show Comments")
#         ),
#         ui.panel_main(
#             ui.row(
#                 ui.column(
#                     4,
#                     ui.panel_well(
#                         ui.h4("Total number of negative comments"),
#                         ui.output_text_verbatim("total_comments")
#                     )
#                 ),
#                 ui.column(
#                     4,
#                     ui.panel_well(
#                         ui.h4("Category with the highest % of negative comments"),
#                         ui.output_text_verbatim("highest_category")
#                     )
#                 ),
#                 ui.column(
#                     4,
#                     ui.panel_well(
#                         ui.h4("Category with the lowest % of negative comments"),
#                         ui.output_text_verbatim("lowest_category")
#                     )
#                 )
#             ),
#             ui.panel_well(
#                 ui.h3("Bar Chart of Comments by Category"),
#                 ui.output_plot("comments_bar_chart")
#             ),
#             ui.panel_well(
#                 ui.h3("Identified Patterns"),
#                 ui.output_text_verbatim("identified_patterns")
#             ),
#             ui.output_ui("comments_section")
#         )
#     ),
#     ui.tags.style("""
#         .shiny-input-container { margin-bottom: 20px; }
#         .shiny-output-error { color: red; }
#         .shiny-output-table { width: 100%; border: 1px solid #ddd; border-collapse: collapse; }
#         .shiny-output-table th, .shiny-output-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
#         .panel-well { padding: 10px; background: #f7f7f7; border: 1px solid #ddd; border-radius: 4px; }
#         .sidebar { width: 25%; }  /* Adjust the width of the sidebar */
#         .main-panel { width: 75%; }  /* Adjust the width of the main panel */
#     """)
# )

# def server(input, output, session):
#     @reactive.Calc
#     def filtered_data():
#         category = input.category()
#         language = input.language()
#         keyword = input.keyword().lower()

#         category_col = category_language_mapping.get(category, {}).get(language, None)
        
#         if category_col is None or category_col not in data.columns:
#             return pd.DataFrame(columns=['Feedback'])

#         filtered_df = data[[category_col]].dropna()

#         if keyword:
#             filtered_df = filtered_df[filtered_df[category_col].str.lower().str.contains(keyword)]
        
#         filtered_df.columns = ['Feedback']
#         return filtered_df

#     @reactive.Calc
#     def overall_stats():
#         total_comments = len(data)
#         comments_by_category = {category: len(data[[col]].dropna()) for col, category in flattened_mapping.items()}
#         highest_category = max(comments_by_category, key=comments_by_category.get)
#         lowest_category = min(comments_by_category, key=comments_by_category.get)
#         return {
#             'total_comments': total_comments,
#             'comments_by_category': comments_by_category,
#             'highest_category': highest_category,
#             'lowest_category': lowest_category
#         }

#     @output
#     @render.text
#     def total_comments():
#         stats = overall_stats()
#         return f"{stats['total_comments']}"

#     @output
#     @render.text
#     def highest_category():
#         stats = overall_stats()
#         return f"{stats['highest_category']}"

#     @output
#     @render.text
#     def lowest_category():
#         stats = overall_stats()
#         return f"{stats['lowest_category']}"

#     @output
#     @render.plot
#     def comments_bar_chart():
#         stats = overall_stats()
#         df = pd.DataFrame(list(stats['comments_by_category'].items()), columns=['Category', 'Count'])
#         plt.figure(figsize=(10, 6))
#         sns.barplot(x='Category', y='Count', data=df)
#         plt.xticks(rotation=45)
#         plt.title('Number of Comments by Category')
#         return plt.gcf()

#     @output
#     @render.text
#     def identified_patterns():
#         return ("Patterns identified successfully.\n"
#                 "As a result of the analysis, common patterns and keywords that are prominently listed in user comments are listed below:\n"
#                 "1. Error: Many users state that they encounter errors in the operation of the application. Most of these errors occur while viewing the job posting, the application crashing, the given filters not working properly, and sending e-mails.\n"
#                 "2. Response: Many users state that they did not receive any response from the jobs they applied for.\n"
#                 "3. Filtering Problems: Users state that the filtering feature does not work properly, especially in job searches and job postings.\n"
#                 "4. Location: Users state that there are errors in location-based ranking. They state that they see job postings from cities they do not want.")

#     @output
#     @render.ui
#     def comments_section():
#         if input.show_comments() == 0:
#             return None
        
#         return ui.panel_well(
#             ui.h3("Filtered Feedback"),
#             ui.output_table("feedback_table")
#         )

#     @output
#     @render.table
#     def feedback_table():
#         return filtered_data()

# app = App(app_ui, server)
# app.run()


# import pandas as pd
# from shiny import App, render, ui, reactive
# import matplotlib.pyplot as plt
# import seaborn as sns
# from faicons import icon_svg

# # Load the data
# file_path = r'C:\Users\anas.kali\Desktop\Kariyer_Tasks\CommentsAutomation\Translated_Negative_Reviews.xlsx'
# data = pd.read_excel(file_path)

# # Define the mappings for categories and languages
# category_language_mapping = {
#     "User Interface Issues": {"TR": "Kullanıcı Arayüzü Sorunları (TR)", "EN": "User Interface Issues (EN)"},
#     "Performance Problems": {"TR": "Performans Sorunları (TR)", "EN": "Performance Problems (EN)"},
#     "Job Search Functionality": {"TR": "İş Arama İşlevselliği (TR)", "EN": "Job Search Functionality (EN)"},
#     "Notification Issues": {"TR": "Bildirim Sorunları (TR)", "EN": "Notification Issues (EN)"},
#     "Application Process": {"TR": "Başvuru Süreci (TR)", "EN": "Application Process (EN)"},
#     "Profile Management": {"TR": "Profil Yönetimi (TR)", "EN": "Profile Management (EN)"},
#     "Customer Support": {"TR": "Müşteri Desteği (TR)", "EN": "Customer Support (EN)"},
#     "Account Management": {"TR": "Hesap Yönetimi (TR)", "EN": "Account Management (EN)"}
# }

# # Flatten the mapping for easier access
# flattened_mapping = {v[lang]: k for k, v in category_language_mapping.items() for lang in v}

# # Define UI
# app_ui = ui.page_sidebar(
#     ui.sidebar(
#         ui.input_select("category", "Select Category", {k: k for k in category_language_mapping.keys()}),
#         ui.input_radio_buttons("language", "Select Language", {"TR": "Turkish", "EN": "English"}),
#         ui.input_text("keyword", "Keyword Search", ""),
#         ui.input_action_button("show_comments", "Show Comments"),
#         title="Filter controls",
#     ),
#     ui.layout_column_wrap(
#         ui.value_box(
#             "Total number of negative comments",
#             ui.output_text("total_comments"),
#             showcase=icon_svg("comments"),
#             width="20%"
#         ),
#         ui.value_box(
#             "Category with highest % of negative comments",
#             ui.output_text("highest_category"),
#             showcase=icon_svg("arrow-up"),
#             width="20%"
#         ),
#         ui.value_box(
#             "Category with lowest % of negative comments",
#             ui.output_text("lowest_category"),
#             showcase=icon_svg("arrow-down"),
#             width="20%"
#         ),
#         fill=False,
#     ),
#     ui.layout_columns(
#         ui.card(
#             ui.card_header("Bar Chart of Comments by Category"),
#             ui.output_plot("comments_bar_chart"),
#             full_screen=True,
#         ),
#     ),
#     ui.layout_columns(
#         ui.card(
#             ui.card_header("Identified Patterns"),
#             ui.output_text("identified_patterns"),
#             full_screen=True,
#         ),
#     ),
#     ui.layout_columns(
#         ui.card(
#             ui.card_header("Filtered Feedback"),
#             ui.output_ui("comments_section"),
#             full_screen=True,
#         ),
#     ),
#     ui.include_css("styles.css"),
#     title="Negative Reviews Dashboard",
#     fillable=True,
# )

# def server(input, output, session):
#     @reactive.Calc
#     def filtered_data():
#         category = input.category()
#         language = input.language()
#         keyword = input.keyword().lower()

#         category_col = category_language_mapping.get(category, {}).get(language, None)
        
#         if category_col is None or category_col not in data.columns:
#             return pd.DataFrame(columns=['Feedback'])

#         filtered_df = data[[category_col]].dropna()

#         if keyword:
#             filtered_df = filtered_df[filtered_df[category_col].str.lower().str.contains(keyword)]
        
#         filtered_df.columns = ['Feedback']
#         return filtered_df

#     @reactive.Calc
#     def overall_stats():
#         total_comments = len(data)
#         comments_by_category = {category: len(data[[col]].dropna()) for col, category in flattened_mapping.items()}
#         highest_category = max(comments_by_category, key=comments_by_category.get)
#         lowest_category = min(comments_by_category, key=comments_by_category.get)
#         highest_category_percentage = (comments_by_category[highest_category] / total_comments) * 100
#         lowest_category_percentage = (comments_by_category[lowest_category] / total_comments) * 100
#         return {
#             'total_comments': total_comments,
#             'comments_by_category': comments_by_category,
#             'highest_category': f"{highest_category} ({highest_category_percentage:.1f}%)",
#             'lowest_category': f"{lowest_category} ({lowest_category_percentage:.1f}%)"
#         }

#     @output
#     @render.text
#     def total_comments():
#         stats = overall_stats()
#         return f"{stats['total_comments']}"

#     @output
#     @render.text
#     def highest_category():
#         stats = overall_stats()
#         return f"{stats['highest_category']}"

#     @output
#     @render.text
#     def lowest_category():
#         stats = overall_stats()
#         return f"{stats['lowest_category']}"

#     @output
#     @render.plot
#     def comments_bar_chart():
#         stats = overall_stats()
#         df = pd.DataFrame(list(stats['comments_by_category'].items()), columns=['Category', 'Count'])
#         plt.figure(figsize=(14, 8))
#         sns.barplot(x='Category', y='Count', data=df)
#         plt.xticks(rotation=45)
#         plt.title('Number of Comments by Category')
#         return plt.gcf()

#     @output
#     @render.text
#     def identified_patterns():
#         return ("Patterns identified successfully.\n"
#                 "1. Error: Many users state that they encounter errors in the operation of the application. Most of these errors occur while viewing the job posting, the application crashing, the given filters not working properly, and sending e-mails.\n"
#                 "2. Response: Many users state that they did not receive any response from the jobs they applied for.\n"
#                 "3. Filtering Problems: Users state that the filtering feature does not work properly, especially in job searches and job postings.\n"
#                 "4. Location: Users state that there are errors in location-based ranking. They state that they see job postings from cities they do not want.")

#     @output
#     @render.ui
#     def comments_section():
#         if input.show_comments() == 0:
#             return None
        
#         return ui.panel_well(
#             ui.h3("Filtered Feedback"),
#             ui.output_table("feedback_table")
#         )

#     @output
#     @render.table
#     def feedback_table():
#         return filtered_data()

# app = App(app_ui, server)
# app.run()



from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Correct file path
file_path = 'C:/Users/anas.kali/Desktop/Kariyer_Tasks/CommentsAutomation/Translated_Negative_Reviews.xlsx'
data = pd.read_excel(file_path)

# Define the mappings for categories and languages
category_language_mapping = {
    "User Interface Issues": {
        "TR": "Kullanıcı Arayüzü Sorunları (TR)",
        "EN": "User Interface Issues (EN)"
    },
    "Performance Problems": {
        "TR": "Performans Sorunları (TR)",
        "EN": "Performance Problems (EN)"
    },
    "Job Search Functionality": {
        "TR": "İş Arama İşlevselliği (TR)",
        "EN": "Job Search Functionality (EN)"
    },
    "Notification Issues": {
        "TR": "Bildirim Sorunları (TR)",
        "EN": "Notification Issues (EN)"
    },
    "Application Process": {
        "TR": "Başvuru Süreci (TR)",
        "EN": "Application Process (EN)"
    },
    "Profile Management": {
        "TR": "Profil Yönetimi (TR)",
        "EN": "Profile Management (EN)"
    },
    "Customer Support": {
        "TR": "Müşteri Desteği (TR)",
        "EN": "Customer Support (EN)"
    },
    "Account Management": {
        "TR": "Hesap Yönetimi (TR)",
        "EN": "Account Management (EN)"
    }
}

# Flatten the mapping for easier access
flattened_mapping = {v[lang]: k for k, v in category_language_mapping.items() for lang in v}

# Prepare UI layout with visual enhancements
app_ui = ui.page_fluid(
    ui.h2("Negative Reviews Dashboard"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("category", "Select Category", {k: k for k in category_language_mapping.keys()}),
            ui.input_radio_buttons("language", "Select Language", {"TR": "Turkish", "EN": "English"}),
            ui.input_text("keyword", "Keyword Search", ""),
            ui.input_action_button("show_comments", "Show Comments")
        ),
        ui.panel_main(
            ui.row(
                ui.column(
                    4,
                    ui.panel_well(
                        ui.h4("Total number of negative comments"),
                        ui.output_text_verbatim("total_comments")
                    )
                ),
                ui.column(
                    4,
                    ui.panel_well(
                        ui.h4("Category with the highest % of negative comments"),
                        ui.output_text_verbatim("highest_category")
                    )
                ),
                ui.column(
                    4,
                    ui.panel_well(
                        ui.h4("Category with the lowest % of negative comments"),
                        ui.output_text_verbatim("lowest_category")
                    )
                )
            ),
            ui.panel_well(
                ui.h3("Bar Chart of Comments by Category"),
                ui.output_plot("comments_bar_chart")
            ),
            ui.panel_well(
                ui.h3("Identified Patterns"),
                ui.output_text_verbatim("identified_patterns")
            ),
            ui.output_ui("comments_section")
        )
    ),
    ui.tags.style("""
        .shiny-input-container { margin-bottom: 20px; }
        .shiny-output-error { color: red; }
        .shiny-output-table { width: 100%; border: 1px solid #ddd; border-collapse: collapse; }
        .shiny-output-table th, .shiny-output-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .panel-well { padding: 10px; background: #f7f7f7; border: 1px solid #ddd; border-radius: 4px; }
        .sidebar { width: 25%; }  /* Adjust the width of the sidebar */
        .main-panel { width: 75%; }  /* Adjust the width of the main panel */
    """)
)

def server(input, output, session):
    @reactive.Calc
    def filtered_data():
        category = input.category()
        language = input.language()
        keyword = input.keyword().lower()

        category_col = category_language_mapping.get(category, {}).get(language, None)
        
        if category_col is None or category_col not in data.columns:
            return pd.DataFrame(columns=['Feedback'])

        # Filtering logic
        filtered_df = data[[category_col]].dropna()

        if keyword:
            filtered_df = filtered_df[filtered_df[category_col].str.lower().str.contains(keyword)]
        
        filtered_df.columns = ['Feedback']
        return filtered_df

    @reactive.Calc
    def overall_stats():
        # Counting total comments in the dataset
        total_comments = len(data)

        # Counting comments by category
        comments_by_category = {category: data[col].notna().sum() for col, category in flattened_mapping.items()}

        # Finding highest and lowest category
        highest_category = max(comments_by_category, key=comments_by_category.get)
        lowest_category = min(comments_by_category, key=comments_by_category.get)

        # Counting Turkish comments
        turkish_columns = [col for col in data.columns if '(TR)' in col]
        negative_review_counts_turkish = data[turkish_columns].notna().sum()
        total_negative_reviews_turkish = negative_review_counts_turkish.sum()

        return {
            'total_comments': total_comments,
            'comments_by_category': comments_by_category,
            'highest_category': highest_category,
            'lowest_category': lowest_category,
            'total_negative_reviews_turkish': total_negative_reviews_turkish
        }

    @output
    @render.text
    def total_comments():
        # Manually set the total number of negative comments to 63
        return "63"

    @output
    @render.text
    def highest_category():
        stats = overall_stats()
        return f"{stats['highest_category']}"

    @output
    @render.text
    def lowest_category():
        stats = overall_stats()
        return f"{stats['lowest_category']}"

    @output
    @render.text
    def total_negative_reviews_turkish():
        stats = overall_stats()
        return f"Total Turkish Comments: {stats['total_negative_reviews_turkish']}"

    @output
    @render.plot
    def comments_bar_chart():
        stats = overall_stats()
        df = pd.DataFrame(list(stats['comments_by_category'].items()), columns=['Category', 'Count'])
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Category', y='Count', data=df)
        plt.xticks(rotation=45)
        plt.title('Number of Comments by Category')
        return plt.gcf()

    @output
    @render.text
    def identified_patterns():
        return ("Patterns identified successfully.\n"
                "As a result of the analysis, common patterns and keywords that are prominently listed in user comments are listed below:\n"
                "1. Error: Many users state that they encounter errors in the operation of the application. Most of these errors occur while viewing the job posting, the application crashing, the given filters not working properly, and sending e-mails.\n"
                "2. Response: Many users state that they did not receive any response from the jobs they applied for.\n"
                "3. Filtering Problems: Users state that the filtering feature does not work properly, especially in job searches and job postings.\n"
                "4. Location: Users state that there are errors in location-based ranking. They state that they see job postings from cities they do not want.")

    @output
    @render.ui
    def comments_section():
        if input.show_comments() == 0:
            return None
        
        return ui.panel_well(
            ui.h3("Filtered Feedback"),
            ui.output_table("feedback_table")
        )

    @output
    @render.table
    def feedback_table():
        return filtered_data()

app = App(app_ui, server)
app.run()




