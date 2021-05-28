/******************************************************************************

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, PHP, Ruby, 
C#, VB, Perl, Swift, Prolog, Javascript, Pascal, HTML, CSS, JS
Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "2020-12-01- Pulakandam-Lesson",
      "provenance": [],
      "collapsed_sections": [],
      "toc_visible": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "W0l8coGdmyaI"
      },
      "source": [
        "# Lesson 0: COVID-19 Outbreak Analysis"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "wf5ibdMS8C8W"
      },
      "source": [
        "### Teacher-Student Activities\n",
        "\n",
        "We all know that coronavirus is spreading on a daily basis in India. So, let's try to visualise how fast it is spreading.\n",
        "\n",
        "First, let's look at the dashboard created by Johns Hopkins University. You can look at the following live dashboard to see the real-time trend.\n",
        "\n",
        "[COVID-19 Live Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)\n",
        "\n",
        "Now, let's create a similar map for India using Python to visualise the most affected states in India due to coronavirus. After the class, you can share it with your parents, relatives and friends by sending them the link to the map."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "LH4QfpXOmwyk"
      },
      "source": [
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ZdRaRNsDu37s"
      },
      "source": [
        "**At this point, the student should share/present their screen with the teacher.**"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "4vbg610OmKQj"
      },
      "source": [
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "L_Opp5fyeA6V"
      },
      "source": [
        "#### Activity 1: Run Source Code\n",
        "\n",
        "This is the source code for the map to be created. You will learn to write it after signing up for the applied tech course. Right now, you just have to execute the code."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "fbsMjhp2vZlE",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "a2d7b7c7-a00f-4789-da8f-04c7f2df78a0"
      },
      "source": [
        "# Student Action: Run the code below.\n",
        "# Download data\n",
        "!git clone https://github.com/CSSEGISandData/COVID-19.git\n",
        "\n",
        "# Install 'geocoder'\n",
        "!pip install geocoder\n",
        "\n",
        "# Importing modules\n",
        "import pandas as pd  \n",
        "import matplotlib.pyplot as plt \n",
        "import seaborn as sns\n",
        "import datetime \n",
        "import geocoder\n",
        "import folium\n",
        "from folium import plugins \n",
        "\n",
        "# DataFrame for the world\n",
        "conf_csv = '/content/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'\n",
        "conf_df = pd.read_csv(conf_csv)\n",
        "grouped_conf_df = conf_df.groupby(by = ['Country/Region'], as_index = False).sum()\n",
        "\n",
        "# DataFrame for India\n",
        "india_df = pd.read_csv(\"https://api.covid19india.org/csv/latest/state_wise.csv\")\n",
        "india_df = india_df.iloc[1:36, :]\n",
        "state_latitudes = []\n",
        "state_longitudes = []\n",
        "for i in india_df.index:\n",
        "    state = india_df['State'][i]\n",
        "    state_lat = geocoder.osm(state).lat\n",
        "    state_lng = geocoder.osm(state).lng\n",
        "    state_latitudes.append(state_lat)\n",
        "    state_longitudes.append(state_lng)\n",
        "\n",
        "state_latitudes = pd.Series(data = state_latitudes, index = india_df.index)\n",
        "state_longitudes = pd.Series(data = state_longitudes, index = india_df.index)\n",
        "india_df['Latitude'] = state_latitudes\n",
        "india_df['Longitude'] = state_longitudes\n",
        "\n",
        "# state_coordinates = [(19.7515, 75.7139), # Maharashtra\n",
        "#                     (11.1271, 78.6569), # Tamil Nadu\n",
        "#                     (15.9129, 79.7400), # Andhra Pradesh\n",
        "#                     (15.317, 75.7139), # Karnataka\n",
        "#                     (28.7041, 77.1025), # Delhi\n",
        "#                     (26.8467, 80.9462), # UP\n",
        "#                     (22.9868, 87.8550), # WB\n",
        "#                     (25.0961, 85.3131), # Bihar\n",
        "#                     (18.1124, 79.0193), # Telangana\n",
        "#                     (22.2587, 71.1924), # Gujarat\n",
        "#                     (26.2006, 92.9376), # Assam\n",
        "#                     (27.0238, 74.2179), # Rajasthan\n",
        "#                     (20.9517, 85.0985), # Odisha\n",
        "#                     (29.0588, 76.0856), # Haryana\n",
        "#                     (22.9734, 78.6569), # Madhya Pradesh\n",
        "#                     (10.8505, 76.2711), # Kerala\n",
        "#                     (31.1471, 75.3412), # Punjab\n",
        "#                     (33.7782, 76.5762), # Jammu and Kashmir\n",
        "#                     (23.6102, 85.2799), # Jharkhand\n",
        "#                     (21.2787, 81.8661), # Chattisgarh\n",
        "#                     (30.0668, 79.0193), # Uttarakhand\n",
        "#                     (15.2993, 74.1240), # Goa\n",
        "#                     (23.9408, 91.9882), # Tripura\n",
        "#                     (11.9416, 79.8083), # Puducherry\n",
        "#                     (24.6637, 93.9063), # Manipur\n",
        "#                     (31.1048, 77.1734), # Himachal Pradesh\n",
        "#                     (26.1584, 94.5624), # Nagaland\n",
        "#                     (28.2180, 94.7278), # Arunachal Pradesh\n",
        "#                     (11.7401, 92.6586), # Andaman and Nicobar\n",
        "#                     (34.1700, 77.5800), # Ladakh\n",
        "#                     (30.7333, 76.7794), # Chandigarh\n",
        "#                     (20.1809, 73.0169), # Dadra and Nagar Haveli\n",
        "#                     (25.4670, 91.3662), # Meghalaya\n",
        "#                     (27.5330, 88.5122), # Sikkim\n",
        "#                     (23.1645, 92.9376), # Mizoram\n",
        "#                      ]\n",
        "                  \n",
        "# ind_state_lat = pd.Series([s[0] for s in state_coordinates], index = india_df.index)\n",
        "# ind_state_lng = pd.Series([s[1] for s in state_coordinates], index = india_df.index)\n",
        "\n",
        "# india_df['Latitude'] = ind_state_lat\n",
        "# india_df['Longitude'] = ind_state_lng\n",
        "\n",
        "# DataFrame for the US\n",
        "us_conf_csv = '/content/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'\n",
        "us_conf_df = pd.read_csv(us_conf_csv)\n",
        "us_conf_df = us_conf_df.dropna()\n",
        "grouped_us_conf_df = us_conf_df.groupby(by = ['Combined_Key'], as_index = False).sum()\n",
        "\n",
        "# Function to get total confirmed cases in a country\n",
        "def get_total_confirmed_cases_for_country(country_name):\n",
        "    total_cases_country = conf_df[conf_df['Country/Region'] == country_name].iloc[:, 4:].apply(sum, axis = 0)\n",
        "    total_cases_country.index = pd.to_datetime(total_cases_country.index)\n",
        "    return total_cases_country\n",
        "\n",
        "# Function to get total confirmed cases in the world\n",
        "def get_total_confirmed_global_cases():\n",
        "    global_cases = conf_df.iloc[:, 4:].apply(sum, axis=0)\n",
        "    global_cases.index = pd.to_datetime(global_cases.index)\n",
        "    return global_cases\n",
        "\n",
        "# Function to create a line plot\n",
        "def line_plot(your_name, plot_background, fig_width, fig_height, country_name, colour, linewidth, markertype):\n",
        "    dt_series = None\n",
        "    if country_name != 'global':\n",
        "        dt_series = get_total_confirmed_cases_for_country(country_name)\n",
        "    else:\n",
        "        dt_series = get_total_confirmed_global_cases()\n",
        "    plt.style.use(plot_background)\n",
        "    plt.figure(figsize = (fig_width, fig_height))\n",
        "    plt.title(f'{country_name.upper()}: Total Coronavirus Cases Reported\\nCreated by {your_name.upper()}\\nPowered by WhiteHat Jr', fontsize = 16)\n",
        "    plt.plot(dt_series.index, dt_series, c = colour, lw = linewidth, marker = markertype, markersize = 7)\n",
        "    plt.xticks(rotation = 45)\n",
        "    plt.ylabel(\"Total Cases\")\n",
        "    plt.grid(linestyle='--', c='grey')\n",
        "    plt.show()\n",
        "\n",
        "# Add minimap\n",
        "def add_minimap(map_name):\n",
        "    # Plugin for mini map\n",
        "    minimap = plugins.MiniMap(toggle_display = True)\n",
        "    map_name.add_child(minimap) # Add minimap\n",
        "    plugins.ScrollZoomToggler().add_to(map_name) # Add scroll zoom toggler to map\n",
        "    plugins.Fullscreen(position='topright').add_to(map_name) # Add full screen button to map\n",
        "\n",
        "# Add title to map\n",
        "def add_title(map_name, country, your_name):\n",
        "    title_html = '''\n",
        "        <h2 align=\"center\" style=\"font-size:20px\"><b>Coronavirus Total Confirmed Cases in {}</b></h2>\n",
        "        <h4 align=\"center\" style=\"font-size:16px\"><i>Created by</i> {}</h4>\n",
        "        <h4 align=\"center\" style=\"font-size:16px\"><i>Powered by</i>\n",
        "            <a href=\"https://www.whitehatjr.com/\">WhiteHat Jr</a>\n",
        "        </h4>\n",
        "             '''.format(country, your_name.upper())   \n",
        "    return map_name.get_root().html.add_child(folium.Element(title_html))\n",
        "\n",
        "# Function to create folium maps using for India, US and the world\n",
        "def folium_map_with_circles(your_name, country, map_width, map_height, left_margin, top_margin, map_tile, zoom, circle_color, minimap):\n",
        "    last_col = conf_df.columns[-1]\n",
        "    if country == 'India':\n",
        "        india_map = folium.Map(location = [22.3511148, 78.6677428], \n",
        "                               width = map_width, height = map_height,\n",
        "                               left = f\"{left_margin}%\", top = f\"{top_margin}%\",\n",
        "                               tiles = map_tile, zoom_start = zoom)\n",
        "        \n",
        "        if minimap == True:\n",
        "            add_minimap(india_map)\n",
        "    \n",
        "        add_title(india_map, country, your_name)    \n",
        "        for i in india_df.index:\n",
        "            folium.Circle(radius = float(india_df.loc[i, 'Confirmed']) / 3,\n",
        "                          location = [india_df.loc[i, 'Latitude'], india_df.loc[i, 'Longitude']],\n",
        "                          popup = \"{}\\n {}\\n on {}\".format(india_df.loc[i, 'State'], \n",
        "                                                          india_df.loc[i, 'Confirmed'], \n",
        "                                                          india_df.loc[i, 'Last_Updated_Time']),\n",
        "                          \n",
        "                          color = circle_color,\n",
        "                          fill = True).add_to(india_map)\n",
        "        return india_map\n",
        "\n",
        "    elif country == 'US':\n",
        "        us_map = folium.Map(location = [39.381266, -97.922211], \n",
        "                            width = map_width, height = map_height, \n",
        "                            left = f\"{left_margin}%\", top = f\"{top_margin}%\",\n",
        "                            tiles = map_tile, zoom_start = zoom)\n",
        "        if minimap == True:\n",
        "            add_minimap(us_map)\n",
        "        \n",
        "        add_title(us_map, country, your_name)\n",
        "        for i in grouped_us_conf_df.index:\n",
        "            folium.Circle(location = [grouped_us_conf_df.loc[i, 'Lat'], grouped_us_conf_df.loc[i, 'Long_']], \n",
        "                          radius = int(grouped_us_conf_df.loc[i, last_col]), \n",
        "                          popup = \"{}\\n {}\\n on {}\".format(grouped_us_conf_df.loc[i, 'Combined_Key'],\n",
        "                                                          grouped_us_conf_df.loc[i, last_col],\n",
        "                                                          last_col),\n",
        "                          color = circle_color,\n",
        "                          fill = True).add_to(us_map)\n",
        "        return us_map\n",
        "    \n",
        "    elif country == 'World':\n",
        "        world_map = folium.Map(location = [0, 0], \n",
        "                            width = map_width, height = map_height, \n",
        "                            left = f\"{left_margin}%\", top = f\"{top_margin}%\",\n",
        "                            tiles = map_tile, zoom_start = zoom)\n",
        "        if minimap == True:\n",
        "            add_minimap(world_map)\n",
        "        \n",
        "        add_title(world_map, country, your_name)\n",
        "        for i in grouped_conf_df.index:\n",
        "            folium.Circle(location = [grouped_conf_df.loc[i, 'Lat'], grouped_conf_df.loc[i, 'Long']], \n",
        "                          radius = int(grouped_conf_df.loc[i, last_col]) / 2, \n",
        "                          popup = \"{}\\n {}\\n on {}\".format(grouped_conf_df.loc[i, 'Country/Region'],\n",
        "                                                          grouped_conf_df.loc[i, last_col], \n",
        "                                                          last_col),\n",
        "                          color = circle_color, \n",
        "                          fill = True).add_to(world_map)\n",
        "        return world_map\n",
        "    else:\n",
        "        print(\"\\nWrong input! Enter either India, US or World.\\n\")\n",
        "\n",
        "# Total confirmed cases in the descending order.\n",
        "grouped_conf_df = conf_df.groupby(by='Country/Region', as_index=False).sum()\n",
        "desc_grp_conf_df = grouped_conf_df.sort_values(by=conf_df.columns[-1], ascending=False)\n",
        "\n",
        "# Function to create a bar plot displaying the top 10 countries having the most number of coronavirus confirmed cases.\n",
        "def bar_plot(your_name, num_countries, width, height):\n",
        "    last_col = conf_df.columns[-1]\n",
        "    latest_date = datetime.datetime.strptime(last_col, '%m/%d/%y').strftime('%B %d, %Y') # Modify the latest date in the 'Month DD, YYYY' format.\n",
        "    plt.figure(figsize = (width, height))\n",
        "    plt.title(f'Top {num_countries} Countries with Highest COVID-19 Confirmed Cases\\nCreated by {your_name.upper()}\\nPowered by WhiteHat Jr', \n",
        "              fontsize = 16)\n",
        "    sns.barplot(desc_grp_conf_df[last_col].head(num_countries), desc_grp_conf_df['Country/Region'].head(num_countries), orient = 'h')\n",
        "    plt.xlabel(f'Total Confirmed Cases (in millions) as of {latest_date}')\n",
        "    plt.show()\n",
        "\n",
        "# Non-cumulative Confirmed Cases.\n",
        "non_cum_conf_df = desc_grp_conf_df.iloc[:, :4]\n",
        "for i in range(len(desc_grp_conf_df.columns[3:]) - 1):\n",
        "    series = desc_grp_conf_df[desc_grp_conf_df.columns[3 + (i + 1) ]] - desc_grp_conf_df[desc_grp_conf_df.columns[3 + i]]\n",
        "    non_cum_conf_df[desc_grp_conf_df.columns[3 + (i + 1)]] = series\n",
        "\n",
        "# Function to get the total non-cumulative confirmed cases in a country.\n",
        "def get_total_daily_confirmed_cases_for_country(country_name):\n",
        "    total_daily_cases = non_cum_conf_df[non_cum_conf_df['Country/Region'] == country_name].iloc[:, 4:].apply(sum, axis = 0)\n",
        "    total_daily_cases.index = pd.to_datetime(total_daily_cases.index)\n",
        "    return total_daily_cases\n",
        "\n",
        "# Line plot for the daily (non-cumulative) confirmed cases in various countries.\n",
        "def daily_cases_line_plot(your_name, num_countries, width, height):\n",
        "    plt.figure(figsize=(width, height))\n",
        "    plt.title(f'Non-Cumulative COVID-19 Confirmed Cases\\nCreated by {your_name.upper()}\\nPowered by WhiteHat Jr', fontsize = 16)\n",
        "    for region in non_cum_conf_df.iloc[:num_countries, :]['Country/Region']:\n",
        "        total_conf_cases = get_total_daily_confirmed_cases_for_country(region)\n",
        "        plt.plot(total_conf_cases.index[53:], total_conf_cases[53:], lw=2.5, label=region)\n",
        "    plt.xticks(rotation=45)\n",
        "    plt.legend()\n",
        "    plt.grid('major', linestyle='--', c='grey')\n",
        "    plt.show()"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Cloning into 'COVID-19'...\n",
            "remote: Enumerating objects: 139626, done.\u001b[K\n",
            "remote: Counting objects: 100% (986/986), done.\u001b[K\n",
            "remote: Compressing objects: 100% (603/603), done.\u001b[K\n",
            "remote: Total 139626 (delta 414), reused 944 (delta 381), pack-reused 138640\u001b[K\n",
            "Receiving objects: 100% (139626/139626), 1.29 GiB | 27.22 MiB/s, done.\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "gg0S_PoPIWNa"
      },
      "source": [
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "pbKvEaCufa-p"
      },
      "source": [
        "#### Activity 2: Line Plot^\n",
        "\n",
        "Let's create a line plot to visualise the total number of confirmed cases in India till yesterday. For the line plot, the dataset that we have on coronavirus is maintained at Johns Hopkins University which gets according to the US time. Hence, we have data updated till yesterday. \n",
        "\n",
        "To view this dataset, write `conf_df[conf_df['Country/Region'] == 'India']` in the code cell below."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qpXGILXhk64L"
      },
      "source": [
        "# Student Action: Write conf_df[conf_df['Country/Region'] == 'India'] to view the dataset for India that will be used to create a line plot.\n",
        "conf_df[conf_df['Country/Region'] == 'India']\n",
        "\n",
        "\n"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "uObwYzKCHHiK"
      },
      "source": [
        "So, in this dataset, we have data for the total confirmed cases in India starting from January 22, 2020. The date given here is in the `MM/DD/YY` format where \n",
        "\n",
        "- `MM` stands for month\n",
        "\n",
        "- `DD` stands for day\n",
        "\n",
        "- `YY` stands for year\n",
        "\n",
        "Now, let's create a line plot. To create a line plot, you need to use the `line_plot()` function which takes the following inputs:\n",
        "\n",
        "- Name of the person who is creating the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`).\n",
        "\n",
        "- The background style of the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`).. Here is the list of most commonly used background styles:\n",
        "\n",
        "  1. `'dark_background'` (most preferred)\n",
        "\n",
        "  2. `'ggplot'`\n",
        "\n",
        "  3. `'seaborn'`\n",
        "\n",
        "  4. `'fivethirtyeight'`\n",
        "\n",
        "  and many more.\n",
        "\n",
        "- Width of the line plot (numeric value).\n",
        "\n",
        "- Height of the line plot (numeric value).\n",
        "\n",
        "- Name of the country which should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`).\n",
        "\n",
        "- Colour of the lines which should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`). Here's the list of most commonly used colours:\n",
        "\n",
        "  1. `'red'`\n",
        "  \n",
        "  2. `'cyan'` \n",
        "  \n",
        "  3. `'magenta'`\n",
        "\n",
        "  4. `'yellow'`\n",
        "\n",
        "  5. `'green'`\n",
        "\n",
        "- The width of the line (numeric value)\n",
        "\n",
        "- The marker style on the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`). Here is the list of the most commonly used marker styles:\n",
        "\n",
        "  1. `'o'` for a circular marker\n",
        "\n",
        "  2. `'*'` for a starred marker\n",
        "\n",
        "  3. `'^'` for a upper triangular marker\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "G1HArsXcHNXK",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 223
        },
        "outputId": "4e1421f9-1640-4242-e668-b047618d5849"
      },
      "source": [
        "# Student Action: Create a line plot for the total confirmed cases in India using the 'line_plot()' function.\n",
        "line_plot(\"hemanth\",'seaborn',17,4,'India','green',3,'*')\n"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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2ze0tLTg1KlT+PLlCxYWFmBZlsvTeo/68akpj1ryqSmPWjpDXfnUlEct+dSUJ51b6vZyhwUCAYTDYVRVVQEA3r17h4GBAZw+fRp5eXmYmZnBmzdv0N7ejm3btrk8rfeoH5+a8qgln5ryqKUz1JVPTXnUkk9NedK5pa50OywQCKC2tnbl9ebNm5FKpQAAtm3DsixcvHjRrfE8T/341JRHLfnUlEctnaGufGrKo5Z8asqTzi0z3B4g3YRCIVRWVuLVq1fo6elBTU2N2yOtK+rHp6Y8asmnpjxq6Qx15VNTHrXkU1OedGrpM8YYt4dIJzMzM2hsbERZWRmuXr267o+/X2vqx6emPGrJp6Y8aukMdeVTUx615FNTnnRqqWe611hubi5s28bJkydRWlrq9jjrjvrxqSmPWvKpKY9aOkNd+dSURy351JQnnVrqSrcLbNtGZqYep/9/qR+fmvKoJZ+a8qilM9SVT0151JJPTXnSpaWWbhERERERERGH6CA1EREREREREYdo6RYRERERERFxiJZuEREREREREYdo6RYRERERERFxiJZuEREREREREYdo6RYRERERERFxyP8ASoaqFsMXhEEAAAAASUVORK5CYII=\n",
            "text/plain": [
              "<Figure size 1224x288 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2uQJGNR1lJBz"
      },
      "source": [
        "**Note:** The `line_plot()` function is NOT a standard Python function. It is a user-defined function created at WhiteHat Jr using Python to simplify the line plot creation process. You will learn to create your own user-defined function in the subsequent classes in this course."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Rt79o-Ork9BO"
      },
      "source": [
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "bb1A1XTZDyxv"
      },
      "source": [
        "#### Activity 3: Map^^\n",
        "\n",
        "Let's create a map for India. For this, we are going to use a dataset showing state-wise data for India. To view the first five rows for the total confirmed cases in India, call the `head()` function on the `india_df` variable which stores the data."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "zcbuqGnITevO",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 394
        },
        "outputId": "1ec77606-f40b-4e8a-d9de-277c26a52260"
      },
      "source": [
        "# Student Action: List the first five rows of the dataset containing the total number of confirmed cases in\n",
        "india_df.head()\n",
        "\n",
        "\n"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>State</th>\n",
              "      <th>Confirmed</th>\n",
              "      <th>Recovered</th>\n",
              "      <th>Deaths</th>\n",
              "      <th>Active</th>\n",
              "      <th>Last_Updated_Time</th>\n",
              "      <th>Migrated_Other</th>\n",
              "      <th>State_code</th>\n",
              "      <th>Delta_Confirmed</th>\n",
              "      <th>Delta_Recovered</th>\n",
              "      <th>Delta_Deaths</th>\n",
              "      <th>State_Notes</th>\n",
              "      <th>Latitude</th>\n",
              "      <th>Longitude</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Maharashtra</td>\n",
              "      <td>1823896</td>\n",
              "      <td>1685122</td>\n",
              "      <td>47151</td>\n",
              "      <td>90557</td>\n",
              "      <td>30/11/2020 20:29:53</td>\n",
              "      <td>1066</td>\n",
              "      <td>MH</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>[Sep 9] :239 cases have been removed from the ...</td>\n",
              "      <td>18.906836</td>\n",
              "      <td>75.674158</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Karnataka</td>\n",
              "      <td>884897</td>\n",
              "      <td>849821</td>\n",
              "      <td>11778</td>\n",
              "      <td>23279</td>\n",
              "      <td>30/11/2020 21:12:19</td>\n",
              "      <td>19</td>\n",
              "      <td>KA</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>14.520390</td>\n",
              "      <td>75.722352</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>Andhra Pradesh</td>\n",
              "      <td>868749</td>\n",
              "      <td>854326</td>\n",
              "      <td>6996</td>\n",
              "      <td>7427</td>\n",
              "      <td>01/12/2020 19:20:50</td>\n",
              "      <td>0</td>\n",
              "      <td>AP</td>\n",
              "      <td>685</td>\n",
              "      <td>1094</td>\n",
              "      <td>4</td>\n",
              "      <td>NaN</td>\n",
              "      <td>15.924091</td>\n",
              "      <td>80.186381</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Tamil Nadu</td>\n",
              "      <td>781915</td>\n",
              "      <td>759206</td>\n",
              "      <td>11712</td>\n",
              "      <td>10997</td>\n",
              "      <td>30/11/2020 20:17:28</td>\n",
              "      <td>0</td>\n",
              "      <td>TN</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>[July 22]: 444 backdated deceased entries adde...</td>\n",
              "      <td>10.909433</td>\n",
              "      <td>78.366535</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>Uttar Pradesh</td>\n",
              "      <td>543888</td>\n",
              "      <td>512028</td>\n",
              "      <td>7761</td>\n",
              "      <td>24099</td>\n",
              "      <td>30/11/2020 20:17:46</td>\n",
              "      <td>0</td>\n",
              "      <td>UP</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>0</td>\n",
              "      <td>NaN</td>\n",
              "      <td>27.130334</td>\n",
              "      <td>80.859666</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "            State  Confirmed  ...   Latitude  Longitude\n",
              "1     Maharashtra    1823896  ...  18.906836  75.674158\n",
              "2       Karnataka     884897  ...  14.520390  75.722352\n",
              "3  Andhra Pradesh     868749  ...  15.924091  80.186381\n",
              "4      Tamil Nadu     781915  ...  10.909433  78.366535\n",
              "5   Uttar Pradesh     543888  ...  27.130334  80.859666\n",
              "\n",
              "[5 rows x 14 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 4
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "eEfwX2AmVl2u"
      },
      "source": [
        "Let's now create a map for India to show the state-wise total confirmed cases of coronavirus. Using the latitude and longitude values (which are numeric values with decimal), we can create circular markers on a map. For this, you need to use the `folium_map_with_circles()` function which takes the following inputs:\n",
        "\n",
        "- Name of the person who is creating the map which should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`).\n",
        "\n",
        "- Name of the country for which a map needs to be created. It should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`). For the map only three values are supported:\n",
        "\n",
        "  1. `'India'`\n",
        "\n",
        "  2. `'US'`\n",
        "\n",
        "  3. `'World'`\n",
        "\n",
        "- Width of the map (numeric value).\n",
        "\n",
        "- Height of the map (numeric value).\n",
        "\n",
        "- Left margin for the map (numeric value).\n",
        "\n",
        "- Top margin for the map (numeric value).\n",
        "\n",
        "- The background style of the line plot which should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`). Here is the list of most commonly used background styles:\n",
        "\n",
        "  1. `'OpenStreetMap'`\n",
        "\n",
        "  2. `'Stamen Terrain'`\n",
        "\n",
        "  3. `'Stamen Toner'`\n",
        "\n",
        "- Initial zoom in value (a numeric value)\n",
        "\n",
        "- Colour of the circles on the map should be a text value enclosed within single-quotes (`''`) or double-quotes (`\"\"`). Here's the list of most commonly used colours:\n",
        "\n",
        "  1. `'red'`\n",
        "  \n",
        "  2. `'blue'` \n",
        "  \n",
        "  3. `'magenta'`\n",
        "\n",
        "  4. `'yellow'`\n",
        "\n",
        "  5. `'green'`\n",
        "\n",
        "- Whether you want the map to have a minimap or not; `True` for **yes** and `False` for **no**.\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "JWAxL5giKQuB",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 394
        },
        "outputId": "fe3b2935-787f-49de-c244-a8851a1c7669"
      },
      "source": [
        "# Student Action: Create a map for India to show the state-wise total confirmed cases of coronavirus\n",
        "folium_map_with_circles(\"hemanth\",\"India\",700,500,1,4,'Stamen Toner',3,'red',True)\n"
      ],
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div style=\"width:100%;\"><div style=\"position:relative;width:100%;height:0;padding-bottom:60%;\"><span style=\"color:#565656\">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe src=\"about:blank\" style=\"position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;\" data-html=PCFET0NUWVBFIGh0bWw+CjxoZWFkPiAgICAKICAgIDxtZXRhIGh0dHAtZXF1aXY9ImNvbnRlbnQtdHlwZSIgY29udGVudD0idGV4dC9odG1sOyBjaGFyc2V0PVVURi04IiAvPgogICAgPHNjcmlwdD5MX1BSRUZFUl9DQU5WQVM9ZmFsc2U7IExfTk9fVE9VQ0g9ZmFsc2U7IExfRElTQUJMRV8zRD1mYWxzZTs8L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS40LjAvZGlzdC9sZWFmbGV0LmpzIj48L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2NvZGUuanF1ZXJ5LmNvbS9qcXVlcnktMS4xMi40Lm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvanMvYm9vdHN0cmFwLm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuanMiPjwvc2NyaXB0PgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS40LjAvZGlzdC9sZWFmbGV0LmNzcyIvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2Jvb3RzdHJhcC8zLjIuMC9jc3MvYm9vdHN0cmFwLm1pbi5jc3MiLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvY3NzL2Jvb3RzdHJhcC10aGVtZS5taW4uY3NzIi8+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vZm9udC1hd2Vzb21lLzQuNi4zL2Nzcy9mb250LWF3ZXNvbWUubWluLmNzcyIvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9MZWFmbGV0LmF3ZXNvbWUtbWFya2Vycy8yLjAuMi9sZWFmbGV0LmF3ZXNvbWUtbWFya2Vycy5jc3MiLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9yYXdjZG4uZ2l0aGFjay5jb20vcHl0aG9uLXZpc3VhbGl6YXRpb24vZm9saXVtL21hc3Rlci9mb2xpdW0vdGVtcGxhdGVzL2xlYWZsZXQuYXdlc29tZS5yb3RhdGUuY3NzIi8+CiAgICA8c3R5bGU+aHRtbCwgYm9keSB7d2lkdGg6IDEwMCU7aGVpZ2h0OiAxMDAlO21hcmdpbjogMDtwYWRkaW5nOiAwO308L3N0eWxlPgogICAgPHN0eWxlPiNtYXAge3Bvc2l0aW9uOmFic29sdXRlO3RvcDowO2JvdHRvbTowO3JpZ2h0OjA7bGVmdDowO308L3N0eWxlPgogICAgCiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLAogICAgICAgIGluaXRpYWwtc2NhbGU9MS4wLCBtYXhpbXVtLXNjYWxlPTEuMCwgdXNlci1zY2FsYWJsZT1ubyIgLz4KICAgIDxzdHlsZT4jbWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0IHsKICAgICAgICBwb3NpdGlvbjogcmVsYXRpdmU7CiAgICAgICAgd2lkdGg6IDcwMC4wcHg7CiAgICAgICAgaGVpZ2h0OiA1MDAuMHB4OwogICAgICAgIGxlZnQ6IDEuMCU7CiAgICAgICAgdG9wOiA0LjAlOwogICAgICAgIH0KICAgIDwvc3R5bGU+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvbGVhZmxldC1taW5pbWFwLzMuNi4xL0NvbnRyb2wuTWluaU1hcC5qcyI+PC9zY3JpcHQ+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vY2RuanMuY2xvdWRmbGFyZS5jb20vYWpheC9saWJzL2xlYWZsZXQtbWluaW1hcC8zLjYuMS9Db250cm9sLk1pbmlNYXAuY3NzIi8+CiAgICAKICAgICAgICAgICAgICAgIDxzdHlsZT4KICAgICAgICAgICAgICAgICAgICAjc2Nyb2xsX3pvb21fdG9nZ2xlcl9kZDYxM2NlY2E2NmY0MWYyODc5NzIwZDczOWMxM2NjYSB7CiAgICAgICAgICAgICAgICAgICAgICAgIHBvc2l0aW9uOmFic29sdXRlOwogICAgICAgICAgICAgICAgICAgICAgICB3aWR0aDozNXB4OwogICAgICAgICAgICAgICAgICAgICAgICBib3R0b206MTBweDsKICAgICAgICAgICAgICAgICAgICAgICAgaGVpZ2h0OjM1cHg7CiAgICAgICAgICAgICAgICAgICAgICAgIGxlZnQ6MTBweDsKICAgICAgICAgICAgICAgICAgICAgICAgYmFja2dyb3VuZC1jb2xvcjojZmZmOwogICAgICAgICAgICAgICAgICAgICAgICB0ZXh0LWFsaWduOmNlbnRlcjsKICAgICAgICAgICAgICAgICAgICAgICAgbGluZS1oZWlnaHQ6MzVweDsKICAgICAgICAgICAgICAgICAgICAgICAgdmVydGljYWwtYWxpZ246IG1pZGRsZTsKICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgPC9zdHlsZT4KICAgICAgICAgICAgCiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvbGVhZmxldC5mdWxsc2NyZWVuLzEuNC4yL0NvbnRyb2wuRnVsbFNjcmVlbi5taW4uanMiPjwvc2NyaXB0PgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9sZWFmbGV0LmZ1bGxzY3JlZW4vMS40LjIvQ29udHJvbC5GdWxsU2NyZWVuLm1pbi5jc3MiLz4KPC9oZWFkPgo8Ym9keT4gICAgCiAgICAKICAgICAgICA8aDIgYWxpZ249ImNlbnRlciIgc3R5bGU9ImZvbnQtc2l6ZToyMHB4Ij48Yj5Db3JvbmF2aXJ1cyBUb3RhbCBDb25maXJtZWQgQ2FzZXMgaW4gSW5kaWE8L2I+PC9oMj4KICAgICAgICA8aDQgYWxpZ249ImNlbnRlciIgc3R5bGU9ImZvbnQtc2l6ZToxNnB4Ij48aT5DcmVhdGVkIGJ5PC9pPiBIRU1BTlRIPC9oND4KICAgICAgICA8aDQgYWxpZ249ImNlbnRlciIgc3R5bGU9ImZvbnQtc2l6ZToxNnB4Ij48aT5Qb3dlcmVkIGJ5PC9pPgogICAgICAgICAgICA8YSBocmVmPSJodHRwczovL3d3dy53aGl0ZWhhdGpyLmNvbS8iPldoaXRlSGF0IEpyPC9hPgogICAgICAgIDwvaDQ+CiAgICAgICAgICAgICAKICAgIAogICAgPGRpdiBjbGFzcz0iZm9saXVtLW1hcCIgaWQ9Im1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCIgPjwvZGl2PgogICAgCiAgICAgICAgICAgIDxpbWcgaWQ9InNjcm9sbF96b29tX3RvZ2dsZXJfZGQ2MTNjZWNhNjZmNDFmMjg3OTcyMGQ3MzljMTNjY2EiIGFsdD0ic2Nyb2xsIgogICAgICAgICAgICAgICAgIHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvaW9uaWNvbnMvMi4wLjEvcG5nLzUxMi9hcnJvdy1tb3ZlLnBuZyIKICAgICAgICAgICAgICAgICBzdHlsZT0iei1pbmRleDogOTk5OTk5IgogICAgICAgICAgICAgICAgIG9uY2xpY2s9Im1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNC50b2dnbGVTY3JvbGwoKSI+CiAgICAgICAgICAgIDwvaW1nPgogICAgICAgICAgICAKPC9ib2R5Pgo8c2NyaXB0PiAgICAKICAgIAogICAgCiAgICAgICAgdmFyIGJvdW5kcyA9IG51bGw7CiAgICAKCiAgICB2YXIgbWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0ID0gTC5tYXAoCiAgICAgICAgJ21hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCcsIHsKICAgICAgICBjZW50ZXI6IFsyMi4zNTExMTQ4LCA3OC42Njc3NDI4XSwKICAgICAgICB6b29tOiAzLAogICAgICAgIG1heEJvdW5kczogYm91bmRzLAogICAgICAgIGxheWVyczogW10sCiAgICAgICAgd29ybGRDb3B5SnVtcDogZmFsc2UsCiAgICAgICAgY3JzOiBMLkNSUy5FUFNHMzg1NywKICAgICAgICB6b29tQ29udHJvbDogdHJ1ZSwKICAgICAgICB9KTsKCgogICAgCiAgICB2YXIgdGlsZV9sYXllcl8yNjk0OWM5YjA2OWM0MDNlOWRlNDhhYjZlZWY4ZGQ0MyA9IEwudGlsZUxheWVyKAogICAgICAgICdodHRwczovL3N0YW1lbi10aWxlcy17c30uYS5zc2wuZmFzdGx5Lm5ldC90b25lci97en0ve3h9L3t5fS5wbmcnLAogICAgICAgIHsKICAgICAgICAiYXR0cmlidXRpb24iOiBudWxsLAogICAgICAgICJkZXRlY3RSZXRpbmEiOiBmYWxzZSwKICAgICAgICAibWF4TmF0aXZlWm9vbSI6IDE4LAogICAgICAgICJtYXhab29tIjogMTgsCiAgICAgICAgIm1pblpvb20iOiAwLAogICAgICAgICJub1dyYXAiOiBmYWxzZSwKICAgICAgICAib3BhY2l0eSI6IDEsCiAgICAgICAgInN1YmRvbWFpbnMiOiAiYWJjIiwKICAgICAgICAidG1zIjogZmFsc2UKfSkuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgIAoKICAgICAgICB2YXIgdGlsZV9sYXllcl84ZTM2ZGRkOWQ3Y2M0YzMwOTE2MDNjOTBiZTBlYTJkYiA9IEwudGlsZUxheWVyKAogICAgICAgICdodHRwczovL3tzfS50aWxlLm9wZW5zdHJlZXRtYXAub3JnL3t6fS97eH0ve3l9LnBuZycsCiAgICAgICAgewogICAgICAgICJhdHRyaWJ1dGlvbiI6IG51bGwsCiAgICAgICAgImRldGVjdFJldGluYSI6IGZhbHNlLAogICAgICAgICJtYXhOYXRpdmVab29tIjogMTgsCiAgICAgICAgIm1heFpvb20iOiAxOCwKICAgICAgICAibWluWm9vbSI6IDAsCiAgICAgICAgIm5vV3JhcCI6IGZhbHNlLAogICAgICAgICJvcGFjaXR5IjogMSwKICAgICAgICAic3ViZG9tYWlucyI6ICJhYmMiLAogICAgICAgICJ0bXMiOiBmYWxzZQp9ICk7CgogICAgICAgIHZhciBtaW5pX21hcF8wZDQyNmM0OTZhMWU0Zjc2ODg4MTBjY2U1YjY3ZTk5NCA9IG5ldyBMLkNvbnRyb2wuTWluaU1hcCggdGlsZV9sYXllcl84ZTM2ZGRkOWQ3Y2M0YzMwOTE2MDNjOTBiZTBlYTJkYiwKICAgICAgICAgewogICJhdXRvVG9nZ2xlRGlzcGxheSI6IGZhbHNlLAogICJjZW50ZXJGaXhlZCI6IGZhbHNlLAogICJjb2xsYXBzZWRIZWlnaHQiOiAyNSwKICAiY29sbGFwc2VkV2lkdGgiOiAyNSwKICAiaGVpZ2h0IjogMTUwLAogICJtaW5pbWl6ZWQiOiBmYWxzZSwKICAicG9zaXRpb24iOiAiYm90dG9tcmlnaHQiLAogICJ0b2dnbGVEaXNwbGF5IjogdHJ1ZSwKICAid2lkdGgiOiAxNTAsCiAgInpvb21BbmltYXRpb24iOiBmYWxzZSwKICAiem9vbUxldmVsRml4ZWQiOiBudWxsLAogICJ6b29tTGV2ZWxPZmZzZXQiOiAtNQp9KTsKICAgICAgICBtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQuYWRkQ29udHJvbChtaW5pX21hcF8wZDQyNmM0OTZhMWU0Zjc2ODg4MTBjY2U1YjY3ZTk5NCk7CgogICAgICAgIAogICAgCiAgICAgICAgICAgICAgICAgICAgbWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0LnNjcm9sbEVuYWJsZWQgPSB0cnVlOwoKICAgICAgICAgICAgICAgICAgICBtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQudG9nZ2xlU2Nyb2xsID0gZnVuY3Rpb24oKSB7CiAgICAgICAgICAgICAgICAgICAgICAgIGlmICh0aGlzLnNjcm9sbEVuYWJsZWQpIHsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc2Nyb2xsRW5hYmxlZCA9IGZhbHNlOwogICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zY3JvbGxXaGVlbFpvb20uZGlzYWJsZSgpOwogICAgICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgICAgICBlbHNlIHsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc2Nyb2xsRW5hYmxlZCA9IHRydWU7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnNjcm9sbFdoZWVsWm9vbS5lbmFibGUoKTsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICAgICAgICAgfTsKCiAgICAgICAgICAgICAgICAgICAgbWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0LnRvZ2dsZVNjcm9sbCgpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICBMLmNvbnRyb2wuZnVsbHNjcmVlbih7CiAgICAgICAgICAgICAgICBwb3NpdGlvbjogJ3RvcHJpZ2h0JywKICAgICAgICAgICAgICAgIHRpdGxlOiAnRnVsbCBTY3JlZW4nLAogICAgICAgICAgICAgICAgdGl0bGVDYW5jZWw6ICdFeGl0IEZ1bGwgU2NyZWVuJywKICAgICAgICAgICAgICAgIGZvcmNlU2VwYXJhdGVCdXR0b246IGZhbHNlLAogICAgICAgICAgICAgICAgfSkuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgbWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0Lm9uKCdlbnRlckZ1bGxzY3JlZW4nLCBmdW5jdGlvbigpewogICAgICAgICAgICAgICAgY29uc29sZS5sb2coJ2VudGVyZWQgZnVsbHNjcmVlbicpOwogICAgICAgICAgICB9KTsKCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfMDJjYjYyYjkxOWMyNDI2YmI4Mjk5YzdlMDM2YWM3YmEgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFsxOC45MDY4MzU2LCA3NS42NzQxNTc5XSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogNjA3OTY1LjMzMzMzMzMzMzQsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF82ZjVhMTdiYTQyMzI0NzQyYTAyY2M0MmE0Mjc2YmY3MSA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF80MjlkZDY3MjQ2ZTA0MWU2YTFiZGNiNjJjYmY1ODM4MSA9ICQoYDxkaXYgaWQ9Imh0bWxfNDI5ZGQ2NzI0NmUwNDFlNmExYmRjYjYyY2JmNTgzODEiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPk1haGFyYXNodHJhICAxODIzODk2ICBvbiAzMC8xMS8yMDIwIDIwOjI5OjUzPC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF82ZjVhMTdiYTQyMzI0NzQyYTAyY2M0MmE0Mjc2YmY3MS5zZXRDb250ZW50KGh0bWxfNDI5ZGQ2NzI0NmUwNDFlNmExYmRjYjYyY2JmNTgzODEpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV8wMmNiNjJiOTE5YzI0MjZiYjgyOTljN2UwMzZhYzdiYS5iaW5kUG9wdXAocG9wdXBfNmY1YTE3YmE0MjMyNDc0MmEwMmNjNDJhNDI3NmJmNzEpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlX2QyNjhhYmRlNjM5NTRhM2FhMGJiMzc2OWM1N2ZkNmU4ID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMTQuNTIwMzg5NiwgNzUuNzIyMzUyMV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDI5NDk2NS42NjY2NjY2NjY3LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfMzE4OTA3YmU0NWI1NDBlZDhkOTAwOWFhMmNlYjk0NTEgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfMTE3N2ExNTdhM2FkNDQ5Y2EzZDhlM2EyNDdlMzM1ODkgPSAkKGA8ZGl2IGlkPSJodG1sXzExNzdhMTU3YTNhZDQ0OWNhM2Q4ZTNhMjQ3ZTMzNTg5IiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5LYXJuYXRha2EgIDg4NDg5NyAgb24gMzAvMTEvMjAyMCAyMToxMjoxOTwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfMzE4OTA3YmU0NWI1NDBlZDhkOTAwOWFhMmNlYjk0NTEuc2V0Q29udGVudChodG1sXzExNzdhMTU3YTNhZDQ0OWNhM2Q4ZTNhMjQ3ZTMzNTg5KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfZDI2OGFiZGU2Mzk1NGEzYWEwYmIzNzY5YzU3ZmQ2ZTguYmluZFBvcHVwKHBvcHVwXzMxODkwN2JlNDViNTQwZWQ4ZDkwMDlhYTJjZWI5NDUxKQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV81Y2ZhZmQyZjNmMjE0OTdiOWU3Y2ZjYzEzYjcyMDFhZSA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzE1LjkyNDA5MDUsIDgwLjE4NjM4MDldLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiAyODk1ODMuMCwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwX2EwN2QzYzVkMzU1NTRkODVhMWY1NzBkMWFkYjkzMGY3ID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sX2E1NjVhYmExOTc4NDQwMjQ5NTY5NDU4ZjBkMjAzYWQ3ID0gJChgPGRpdiBpZD0iaHRtbF9hNTY1YWJhMTk3ODQ0MDI0OTU2OTQ1OGYwZDIwM2FkNyIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+QW5kaHJhIFByYWRlc2ggIDg2ODc0OSAgb24gMDEvMTIvMjAyMCAxOToyMDo1MDwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfYTA3ZDNjNWQzNTU1NGQ4NWExZjU3MGQxYWRiOTMwZjcuc2V0Q29udGVudChodG1sX2E1NjVhYmExOTc4NDQwMjQ5NTY5NDU4ZjBkMjAzYWQ3KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfNWNmYWZkMmYzZjIxNDk3YjllN2NmY2MxM2I3MjAxYWUuYmluZFBvcHVwKHBvcHVwX2EwN2QzYzVkMzU1NTRkODVhMWY1NzBkMWFkYjkzMGY3KQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV84NjE0MWI2MTYxOTY0MDFlYmI2ZGIwMTgyNDgwZTJkNSA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzEwLjkwOTQzMzQsIDc4LjM2NjUzNDddLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiAyNjA2MzguMzMzMzMzMzMzMzQsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF83ZjE1NWU0ODRhN2I0YzI4YjAxNjFkNGIyZmQ4OTRlYiA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF85YzdjMjBmYWI2ZWY0Yjg5OWYzZDFhYTU1NzI2NTI5OSA9ICQoYDxkaXYgaWQ9Imh0bWxfOWM3YzIwZmFiNmVmNGI4OTlmM2QxYWE1NTcyNjUyOTkiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPlRhbWlsIE5hZHUgIDc4MTkxNSAgb24gMzAvMTEvMjAyMCAyMDoxNzoyODwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfN2YxNTVlNDg0YTdiNGMyOGIwMTYxZDRiMmZkODk0ZWIuc2V0Q29udGVudChodG1sXzljN2MyMGZhYjZlZjRiODk5ZjNkMWFhNTU3MjY1Mjk5KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfODYxNDFiNjE2MTk2NDAxZWJiNmRiMDE4MjQ4MGUyZDUuYmluZFBvcHVwKHBvcHVwXzdmMTU1ZTQ4NGE3YjRjMjhiMDE2MWQ0YjJmZDg5NGViKQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV9mNzA0Y2I3NTYyMmE0ZTJkYjVkZWVkYTNiZGEwOTA1MSA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzI3LjEzMDMzNDQsIDgwLjg1OTY2Nl0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDE4MTI5Ni4wLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNjVlODU1OGQ5YmRiNGJkM2I5NTdhZTdjMGVlYmIxN2EgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfYTkxYmQ0ZWUxZmJlNGFiMzgzNjZmZDNkMTVmYTcyOGQgPSAkKGA8ZGl2IGlkPSJodG1sX2E5MWJkNGVlMWZiZTRhYjM4MzY2ZmQzZDE1ZmE3MjhkIiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5VdHRhciBQcmFkZXNoICA1NDM4ODggIG9uIDMwLzExLzIwMjAgMjA6MTc6NDY8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzY1ZTg1NThkOWJkYjRiZDNiOTU3YWU3YzBlZWJiMTdhLnNldENvbnRlbnQoaHRtbF9hOTFiZDRlZTFmYmU0YWIzODM2NmZkM2QxNWZhNzI4ZCk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlX2Y3MDRjYjc1NjIyYTRlMmRiNWRlZWRhM2JkYTA5MDUxLmJpbmRQb3B1cChwb3B1cF82NWU4NTU4ZDliZGI0YmQzYjk1N2FlN2MwZWViYjE3YSkKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfZjliNDg1NWJlMDNmNDkyY2I5OGEyYjQ3NjE4NTgyOTQgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFsxMC4zNTI4NzQ0LCA3Ni41MTIwMzk2XSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogMjAyNzg2LjAsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF83NmQ4Mjk3ODU5ZGE0ZWQyOTZkZDAwMDkxYzlkZTQ0YyA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF80ZTdjYThhNGY5MTg0N2M0OTllMWRhYmY0MWQzOGI2MiA9ICQoYDxkaXYgaWQ9Imh0bWxfNGU3Y2E4YTRmOTE4NDdjNDk5ZTFkYWJmNDFkMzhiNjIiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPktlcmFsYSAgNjA4MzU4ICBvbiAwMS8xMi8yMDIwIDE5OjIxOjQ0PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF83NmQ4Mjk3ODU5ZGE0ZWQyOTZkZDAwMDkxYzlkZTQ0Yy5zZXRDb250ZW50KGh0bWxfNGU3Y2E4YTRmOTE4NDdjNDk5ZTFkYWJmNDFkMzhiNjIpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV9mOWI0ODU1YmUwM2Y0OTJjYjk4YTJiNDc2MTg1ODI5NC5iaW5kUG9wdXAocG9wdXBfNzZkODI5Nzg1OWRhNGVkMjk2ZGQwMDA5MWM5ZGU0NGMpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzA2MDEyZmQwNWQxMDQwZmU5ZTBlNDA4ZDg1ODMwOWFmID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjguNjUxNzE3OCwgNzcuMjIxOTM4OF0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDE5MTQ2MC4wLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfZDA0MGFmYTgyM2Y1NGU5N2EwY2Y5MmIxNDQ5OGQ0MzAgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfZDljNDA2OWU0NzNiNDJkMTk5NWQyZWE4YzIzMGIyZTggPSAkKGA8ZGl2IGlkPSJodG1sX2Q5YzQwNjllNDczYjQyZDE5OTVkMmVhOGMyMzBiMmU4IiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5EZWxoaSAgNTc0MzgwICBvbiAwMS8xMi8yMDIwIDE5OjIwOjU1PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF9kMDQwYWZhODIzZjU0ZTk3YTBjZjkyYjE0NDk4ZDQzMC5zZXRDb250ZW50KGh0bWxfZDljNDA2OWU0NzNiNDJkMTk5NWQyZWE4YzIzMGIyZTgpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV8wNjAxMmZkMDVkMTA0MGZlOWUwZTQwOGQ4NTgzMDlhZi5iaW5kUG9wdXAocG9wdXBfZDA0MGFmYTgyM2Y1NGU5N2EwY2Y5MmIxNDQ5OGQ0MzApCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzI3OGFmMTcxNzAyYjQwNTVhNjNmMTMyNWQyMmQ3YTBkID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjIuOTk2NDk0OCwgODcuNjg1NTg4Ml0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDE2MTE2MS4zMzMzMzMzMzMzNCwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzUzNTRhOTY3NjQ2ZTQ0YWY4ZTY0MGVhZTgwZDA0Yjg2ID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sX2Y4NTg2OGJjOTM0ZjQ4ZGI5ODQ0MGExZmY2YzYwNWQwID0gJChgPGRpdiBpZD0iaHRtbF9mODU4NjhiYzkzNGY0OGRiOTg0NDBhMWZmNmM2MDVkMCIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+V2VzdCBCZW5nYWwgIDQ4MzQ4NCAgb24gMzAvMTEvMjAyMCAyMToxMjoyMTwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfNTM1NGE5Njc2NDZlNDRhZjhlNjQwZWFlODBkMDRiODYuc2V0Q29udGVudChodG1sX2Y4NTg2OGJjOTM0ZjQ4ZGI5ODQ0MGExZmY2YzYwNWQwKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfMjc4YWYxNzE3MDJiNDA1NWE2M2YxMzI1ZDIyZDdhMGQuYmluZFBvcHVwKHBvcHVwXzUzNTRhOTY3NjQ2ZTQ0YWY4ZTY0MGVhZTgwZDA0Yjg2KQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV8zY2YwM2MyMDk0Yjk0MGQ3YTI5MWM5MGQ5MWQxOGU5ZiA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzIwLjU0MzEyNDEsIDg0LjY4OTczMjFdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiAxMDYzNjcuNjY2NjY2NjY2NjcsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF84OTdiMzAzODJlYzY0N2E3ODQyMDMwZWUyOTkwNmRiYSA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF9jZTFiZDEyOTFlMDE0YmZiYjE1NDNlNTM5MTcxMTE3YyA9ICQoYDxkaXYgaWQ9Imh0bWxfY2UxYmQxMjkxZTAxNGJmYmIxNTQzZTUzOTE3MTExN2MiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPk9kaXNoYSAgMzE5MTAzICBvbiAwMS8xMi8yMDIwIDE2OjMwOjQwPC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF84OTdiMzAzODJlYzY0N2E3ODQyMDMwZWUyOTkwNmRiYS5zZXRDb250ZW50KGh0bWxfY2UxYmQxMjkxZTAxNGJmYmIxNTQzZTUzOTE3MTExN2MpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV8zY2YwM2MyMDk0Yjk0MGQ3YTI5MWM5MGQ5MWQxOGU5Zi5iaW5kUG9wdXAocG9wdXBfODk3YjMwMzgyZWM2NDdhNzg0MjAzMGVlMjk5MDZkYmEpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzZhZDg5NzlmOWI0NjQ1M2Y5N2UyYjAyNDBhODhkMzgyID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMTcuODQ5NTkxOSwgNzkuMTE1MTY2M10sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDkwMTA2LjAsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF85ZTMxMDNiZTExM2U0ZGUwYWVhOGFmMzgwMjcxNmEyOSA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF8xMTViMzIzYmIxYTM0ODNhYjQxMmQyNDFlNGE0NzQxYyA9ICQoYDxkaXYgaWQ9Imh0bWxfMTE1YjMyM2JiMWEzNDgzYWI0MTJkMjQxZTRhNDc0MWMiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPlRlbGFuZ2FuYSAgMjcwMzE4ICBvbiAwMS8xMi8yMDIwIDE2OjMwOjQyPC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF85ZTMxMDNiZTExM2U0ZGUwYWVhOGFmMzgwMjcxNmEyOS5zZXRDb250ZW50KGh0bWxfMTE1YjMyM2JiMWEzNDgzYWI0MTJkMjQxZTRhNDc0MWMpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV82YWQ4OTc5ZjliNDY0NTNmOTdlMmIwMjQwYTg4ZDM4Mi5iaW5kUG9wdXAocG9wdXBfOWUzMTAzYmUxMTNlNGRlMGFlYThhZjM4MDI3MTZhMjkpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzlmODlkMDFkZTNiYzRmZTE4ZGM3Y2UwMDhjNjJlOGU5ID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjUuNjQ0MDg0NSwgODUuOTA2NTA4XSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogNzg2OTkuMzMzMzMzMzMzMzMsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF9iNDU2NzRhNzk0Mjg0YTdmYWEwZTJhMmYzZTgzYmVlNSA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF8xZGZjMzIxMTMyMWE0NTRkOWUxY2UyNzg0MzM1ZjhjYyA9ICQoYDxkaXYgaWQ9Imh0bWxfMWRmYzMyMTEzMjFhNDU0ZDllMWNlMjc4NDMzNWY4Y2MiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPkJpaGFyICAyMzYwOTggIG9uIDAxLzEyLzIwMjAgMTk6MjA6NTg8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwX2I0NTY3NGE3OTQyODRhN2ZhYTBlMmEyZjNlODNiZWU1LnNldENvbnRlbnQoaHRtbF8xZGZjMzIxMTMyMWE0NTRkOWUxY2UyNzg0MzM1ZjhjYyk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlXzlmODlkMDFkZTNiYzRmZTE4ZGM3Y2UwMDhjNjJlOGU5LmJpbmRQb3B1cChwb3B1cF9iNDU2NzRhNzk0Mjg0YTdmYWEwZTJhMmYzZTgzYmVlNSkKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfNDA4ZTRlZTYzMWE3NGMwZGJjM2U4Y2RhYzZjOWYwNDQgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFsyNi44MTA1Nzc3LCA3My43Njg0NTQ5XSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogOTAxMzYuNjY2NjY2NjY2NjcsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF8zOWNlYWJlZWRmN2Q0MTNiYTY1MDYwZjA3MTk1M2ViZiA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF9mZGU4OTM5ZDEyYWM0MjEwOWVkOTM0N2VkMTg5MGZmMSA9ICQoYDxkaXYgaWQ9Imh0bWxfZmRlODkzOWQxMmFjNDIxMDllZDkzNDdlZDE4OTBmZjEiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPlJhamFzdGhhbiAgMjcwNDEwICBvbiAwMS8xMi8yMDIwIDE5OjIxOjQ2PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF8zOWNlYWJlZWRmN2Q0MTNiYTY1MDYwZjA3MTk1M2ViZi5zZXRDb250ZW50KGh0bWxfZmRlODkzOWQxMmFjNDIxMDllZDkzNDdlZDE4OTBmZjEpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV80MDhlNGVlNjMxYTc0YzBkYmMzZThjZGFjNmM5ZjA0NC5iaW5kUG9wdXAocG9wdXBfMzljZWFiZWVkZjdkNDEzYmE2NTA2MGYwNzE5NTNlYmYpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlX2ZmZTM2MDAxZWMxZDRmNTc4ZDY0ZWVmYTJlY2ZiNzgzID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjYuNDA3Mzg0MSwgOTMuMjU1MTMwM10sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDcwOTI1LjMzMzMzMzMzMzMzLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfYTY0MTVmNzMxYzZjNGRkM2E4MzI4N2JmMzQxNzQwMDkgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfZjgwMWUwZjhjNjY3NDVkZmFmN2E0MjE2NTRhZDBkYzcgPSAkKGA8ZGl2IGlkPSJodG1sX2Y4MDFlMGY4YzY2NzQ1ZGZhZjdhNDIxNjU0YWQwZGM3IiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5Bc3NhbSAgMjEyNzc2ICBvbiAzMC8xMS8yMDIwIDIxOjEyOjI0PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF9hNjQxNWY3MzFjNmM0ZGQzYTgzMjg3YmYzNDE3NDAwOS5zZXRDb250ZW50KGh0bWxfZjgwMWUwZjhjNjY3NDVkZmFmN2E0MjE2NTRhZDBkYzcpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV9mZmUzNjAwMWVjMWQ0ZjU3OGQ2NGVlZmEyZWNmYjc4My5iaW5kUG9wdXAocG9wdXBfYTY0MTVmNzMxYzZjNGRkM2E4MzI4N2JmMzQxNzQwMDkpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzBjYjZjNmI0N2MwNDQ3MTBiYzQ3NTRjMzc3YWEzNzhkID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjEuNjYzNzM1OSwgODEuODQwNjM1MV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDc5MTA3LjMzMzMzMzMzMzMzLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNmJkNGY4ZmExOWQxNGEwZDlkMDcyNzRiOGRiMzI1MjcgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfOWVhMGY2NDk0ZjY2NDg1ZTk4NjQzNDgzMzQxMTA2NDAgPSAkKGA8ZGl2IGlkPSJodG1sXzllYTBmNjQ5NGY2NjQ4NWU5ODY0MzQ4MzM0MTEwNjQwIiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5DaGhhdHRpc2dhcmggIDIzNzMyMiAgb24gMzAvMTEvMjAyMCAyMjo1Mjo0MzwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfNmJkNGY4ZmExOWQxNGEwZDlkMDcyNzRiOGRiMzI1Mjcuc2V0Q29udGVudChodG1sXzllYTBmNjQ5NGY2NjQ4NWU5ODY0MzQ4MzM0MTEwNjQwKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfMGNiNmM2YjQ3YzA0NDcxMGJjNDc1NGMzNzdhYTM3OGQuYmluZFBvcHVwKHBvcHVwXzZiZDRmOGZhMTlkMTRhMGQ5ZDA3Mjc0YjhkYjMyNTI3KQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV8zMWI4ZTU4Nzk0NWU0OWQ0YTU3NDEyNTBkMjllYTFiYyA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzI5LjAsIDc2LjBdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA3ODA0Mi4wLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfN2UyZTQyMTBjNDc0NGFhYjhlNTE5Yjk1OWZlZDFiOTMgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfYjFkMThhMDA0OTU3NDI1NGFlOGYyYzUwZDUwNTllYTQgPSAkKGA8ZGl2IGlkPSJodG1sX2IxZDE4YTAwNDk1NzQyNTRhZThmMmM1MGQ1MDU5ZWE0IiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5IYXJ5YW5hICAyMzQxMjYgIG9uIDMwLzExLzIwMjAgMjA6MTg6MDg8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzdlMmU0MjEwYzQ3NDRhYWI4ZTUxOWI5NTlmZWQxYjkzLnNldENvbnRlbnQoaHRtbF9iMWQxOGEwMDQ5NTc0MjU0YWU4ZjJjNTBkNTA1OWVhNCk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlXzMxYjhlNTg3OTQ1ZTQ5ZDRhNTc0MTI1MGQyOWVhMWJjLmJpbmRQb3B1cChwb3B1cF83ZTJlNDIxMGM0NzQ0YWFiOGU1MTliOTU5ZmVkMWI5MykKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfNjI4NDg3NjFhZWU5NGU0OWE5ZWVjMzlhN2QyODNmODMgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFsyMi40MTU0MDgyNSwgNzIuMDMxNDk3MDM2OTkyODJdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA2OTkyNi42NjY2NjY2NjY2NywKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwX2MzN2VlNzJjMDc4ZDQ5Nzg4YjNhNDAwYjNlYzZkNDc0ID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzZmNWE0MGFmYTcwZTRhOTY5ZWZmZjU1NzNkZDExODVmID0gJChgPGRpdiBpZD0iaHRtbF82ZjVhNDBhZmE3MGU0YTk2OWVmZmY1NTczZGQxMTg1ZiIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+R3VqYXJhdCAgMjA5NzgwICBvbiAzMC8xMS8yMDIwIDIwOjE4OjUzPC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF9jMzdlZTcyYzA3OGQ0OTc4OGIzYTQwMGIzZWM2ZDQ3NC5zZXRDb250ZW50KGh0bWxfNmY1YTQwYWZhNzBlNGE5NjllZmZmNTU3M2RkMTE4NWYpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV82Mjg0ODc2MWFlZTk0ZTQ5YTllZWMzOWE3ZDI4M2Y4My5iaW5kUG9wdXAocG9wdXBfYzM3ZWU3MmMwNzhkNDk3ODhiM2E0MDBiM2VjNmQ0NzQpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzgzNTIzMWExNTA5ZTQxZjNhNzk2NTUxMTg3N2FjY2JiID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjMuOTY5OTI4MiwgNzkuMzk0ODY5NTQ2MjUyMjVdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA2ODcwOS4zMzMzMzMzMzMzMywKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzBiMzcyYzhiYjMwNTQzYjk5ZjU1NzliYjQ0MTFmZjljID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzNiNTg3ZTllOWVkMjRhOTZiN2YwOGU1OTFhMjM3MTBkID0gJChgPGRpdiBpZD0iaHRtbF8zYjU4N2U5ZTllZDI0YTk2YjdmMDhlNTkxYTIzNzEwZCIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+TWFkaHlhIFByYWRlc2ggIDIwNjEyOCAgb24gMzAvMTEvMjAyMCAyMDoxOTowNjwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfMGIzNzJjOGJiMzA1NDNiOTlmNTU3OWJiNDQxMWZmOWMuc2V0Q29udGVudChodG1sXzNiNTg3ZTllOWVkMjRhOTZiN2YwOGU1OTFhMjM3MTBkKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfODM1MjMxYTE1MDllNDFmM2E3OTY1NTExODc3YWNjYmIuYmluZFBvcHVwKHBvcHVwXzBiMzcyYzhiYjMwNTQzYjk5ZjU1NzliYjQ0MTFmZjljKQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV9lZmI5OGM3ZTEyMjc0NzY2OWM1OTE0NmVjNmI0ZWRlMiA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzMwLjkyOTMyMTEsIDc1LjUwMDQ4NDFdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA1MDY5Ny4wLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfZDBiMjM3NDcxMDgzNDk5Njk4NTI3MmMxYWJhNzJlNTYgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfODQyNTI4ZjI1MzY1NGJlYmJjMzYwYzZmYTkxZjFhMWMgPSAkKGA8ZGl2IGlkPSJodG1sXzg0MjUyOGYyNTM2NTRiZWJiYzM2MGM2ZmE5MWYxYTFjIiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5QdW5qYWIgIDE1MjA5MSAgb24gMzAvMTEvMjAyMCAyMDo1MDowODwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfZDBiMjM3NDcxMDgzNDk5Njk4NTI3MmMxYWJhNzJlNTYuc2V0Q29udGVudChodG1sXzg0MjUyOGYyNTM2NTRiZWJiYzM2MGM2ZmE5MWYxYTFjKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfZWZiOThjN2UxMjI3NDc2NjljNTkxNDZlYzZiNGVkZTIuYmluZFBvcHVwKHBvcHVwX2QwYjIzNzQ3MTA4MzQ5OTY5ODUyNzJjMWFiYTcyZTU2KQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV8wNGVjMjc5NDA4NGE0MGI3YjY4MmJkMWVhYTk0ZTQ5MyA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzIzLjQ1NTk4MDksIDg1LjI1NTczMDFdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiAzNjM4My42NjY2NjY2NjY2NjQsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF9hNmM1MjUxOTYyZjM0ZjUzYmVhYjI3NmQ0M2ZjNjNmYSA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF9jZmNhNWI1MjVlYWE0NzM2YmUzMmNjMjA4NTE4YmFjNiA9ICQoYDxkaXYgaWQ9Imh0bWxfY2ZjYTViNTI1ZWFhNDczNmJlMzJjYzIwODUxOGJhYzYiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPkpoYXJraGFuZCAgMTA5MTUxICBvbiAzMC8xMS8yMDIwIDIxOjIyOjM1PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF9hNmM1MjUxOTYyZjM0ZjUzYmVhYjI3NmQ0M2ZjNjNmYS5zZXRDb250ZW50KGh0bWxfY2ZjYTViNTI1ZWFhNDczNmJlMzJjYzIwODUxOGJhYzYpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV8wNGVjMjc5NDA4NGE0MGI3YjY4MmJkMWVhYTk0ZTQ5My5iaW5kUG9wdXAocG9wdXBfYTZjNTI1MTk2MmYzNGY1M2JlYWIyNzZkNDNmYzYzZmEpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlX2ZjYWFlMzA1NmJkZjRhYTRhZTdlNWNmNTUxNjNlYzNhID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMzMuNTU3NDQ3MywgNzUuMDYxNTJdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiAzNjg5Mi42NjY2NjY2NjY2NjQsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF8xM2E0ZDM0MTNhOTk0YmZkOGU0N2I0ZjMwZjk4NzQ2ZiA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF8yNjE2MTgzODBjZWI0YzhjYjZhYjgwYWZmYmM0MDNjZCA9ICQoYDxkaXYgaWQ9Imh0bWxfMjYxNjE4MzgwY2ViNGM4Y2I2YWI4MGFmZmJjNDAzY2QiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPkphbW11IGFuZCBLYXNobWlyICAxMTA2NzggIG9uIDAxLzEyLzIwMjAgMTk6MjE6MDM8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzEzYTRkMzQxM2E5OTRiZmQ4ZTQ3YjRmMzBmOTg3NDZmLnNldENvbnRlbnQoaHRtbF8yNjE2MTgzODBjZWI0YzhjYjZhYjgwYWZmYmM0MDNjZCk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlX2ZjYWFlMzA1NmJkZjRhYTRhZTdlNWNmNTUxNjNlYzNhLmJpbmRQb3B1cChwb3B1cF8xM2E0ZDM0MTNhOTk0YmZkOGU0N2I0ZjMwZjk4NzQ2ZikKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfZWU1ODJiZThmZTRiNDhkZjg5NjM1MGFiMzI4OGI3YTYgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFszMC4wOTE5OTM1NDk5OTk5OTgsIDc5LjMyMTc2NjU5MzQzMDE4XSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogMjUwOTcuMzMzMzMzMzMzMzMyLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfY2Y0OWJlYjMyYzQ2NDAzYjg2MGJmNWY0YTIxMzdiOTQgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfYWJhNDdjZTkyODY5NDRiOWFhZmI5YTAzZjUwODUzZGYgPSAkKGA8ZGl2IGlkPSJodG1sX2FiYTQ3Y2U5Mjg2OTQ0YjlhYWZiOWEwM2Y1MDg1M2RmIiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5VdHRhcmFraGFuZCAgNzUyOTIgIG9uIDAxLzEyLzIwMjAgMTk6MzM6NTM8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwX2NmNDliZWIzMmM0NjQwM2I4NjBiZjVmNGEyMTM3Yjk0LnNldENvbnRlbnQoaHRtbF9hYmE0N2NlOTI4Njk0NGI5YWFmYjlhMDNmNTA4NTNkZik7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlX2VlNTgyYmU4ZmU0YjQ4ZGY4OTYzNTBhYjMyODhiN2E2LmJpbmRQb3B1cChwb3B1cF9jZjQ5YmViMzJjNDY0MDNiODYwYmY1ZjRhMjEzN2I5NCkKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfZTMyNmIzODM1MTkxNDhjZmJmZDAwZWQyMjU3NzEzZjkgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFsxNS4zMDA0NTQzLCA3NC4wODU1MTM0XSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogMTU5ODcuNjY2NjY2NjY2NjY2LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfMGU3OWFlYzc2YjE0NGMyYzgyMDZlZTA5OGYzZjI3MDAgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfYTE2YjUyODE3MTU4NDU4YmEwYTUwYzdhNTRiZjFkODggPSAkKGA8ZGl2IGlkPSJodG1sX2ExNmI1MjgxNzE1ODQ1OGJhMGE1MGM3YTU0YmYxZDg4IiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5Hb2EgIDQ3OTYzICBvbiAzMC8xMS8yMDIwIDIwOjUwOjE0PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF8wZTc5YWVjNzZiMTQ0YzJjODIwNmVlMDk4ZjNmMjcwMC5zZXRDb250ZW50KGh0bWxfYTE2YjUyODE3MTU4NDU4YmEwYTUwYzdhNTRiZjFkODgpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV9lMzI2YjM4MzUxOTE0OGNmYmZkMDBlZDIyNTc3MTNmOS5iaW5kUG9wdXAocG9wdXBfMGU3OWFlYzc2YjE0NGMyYzgyMDZlZTA5OGYzZjI3MDApCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzFiODczZDA4ZmY1ODQwZTZiYmFhZmI0OTY3Zjc4ZGNhID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMTEuOTM0MDU2OCwgNzkuODMwNjQ0N10sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDEyMzIyLjY2NjY2NjY2NjY2NiwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzQzNmY0NGExYmQyMTQ0NDg4ZGYxNjZhMjQ3ZDkyOGJmID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzEyMTgwYTZkYzA4MzQwMGM5MDNkMGRjNTJiZDRhMmIxID0gJChgPGRpdiBpZD0iaHRtbF8xMjE4MGE2ZGMwODM0MDBjOTAzZDBkYzUyYmQ0YTJiMSIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+UHVkdWNoZXJyeSAgMzY5NjggIG9uIDMwLzExLzIwMjAgMjM6MTM6MjI8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzQzNmY0NGExYmQyMTQ0NDg4ZGYxNjZhMjQ3ZDkyOGJmLnNldENvbnRlbnQoaHRtbF8xMjE4MGE2ZGMwODM0MDBjOTAzZDBkYzUyYmQ0YTJiMSk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlXzFiODczZDA4ZmY1ODQwZTZiYmFhZmI0OTY3Zjc4ZGNhLmJpbmRQb3B1cChwb3B1cF80MzZmNDRhMWJkMjE0NDQ4OGRmMTY2YTI0N2Q5MjhiZikKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfMjM2OTA5NzY4OGFlNDFiOWE0ZTZkMjg1NDE3NTE2NGQgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFsyMy43NzUwODIzLCA5MS43MDI1MDkxXSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogMTA5MDcuNjY2NjY2NjY2NjY2LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfMWQ2MDZkMTk2MWRhNGMwNThkZDFlYWFjODQxNTdlYjUgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfMDY3MzgxMmE3OWYwNGUyZmE5NjZmMTU5NmQ0ZDk0YjYgPSAkKGA8ZGl2IGlkPSJodG1sXzA2NzM4MTJhNzlmMDRlMmZhOTY2ZjE1OTZkNGQ5NGI2IiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5UcmlwdXJhICAzMjcyMyAgb24gMDEvMTIvMjAyMCAxMzoxMjozODwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfMWQ2MDZkMTk2MWRhNGMwNThkZDFlYWFjODQxNTdlYjUuc2V0Q29udGVudChodG1sXzA2NzM4MTJhNzlmMDRlMmZhOTY2ZjE1OTZkNGQ5NGI2KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfMjM2OTA5NzY4OGFlNDFiOWE0ZTZkMjg1NDE3NTE2NGQuYmluZFBvcHVwKHBvcHVwXzFkNjA2ZDE5NjFkYTRjMDU4ZGQxZWFhYzg0MTU3ZWI1KQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV9lYTE5OWE2MDczNTQ0MTdjOTQzZmJkNzllZjlmNDdkYSA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzMxLjgxNjc2MDE1LCA3Ny4zNDkzMjA1MTk2ODg1OF0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDEzNTA2LjAsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF84ZTMyNzlhN2QxMDI0NzM1YjcyOTMxNGNmYTViZDFhNSA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF80MzkyODc3N2JlOTU0YmRjYjk4N2JiNmNjNjU2OGVkMyA9ICQoYDxkaXYgaWQ9Imh0bWxfNDM5Mjg3NzdiZTk1NGJkY2I5ODdiYjZjYzY1NjhlZDMiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPkhpbWFjaGFsIFByYWRlc2ggIDQwNTE4ICBvbiAwMS8xMi8yMDIwIDA0OjI5OjQxPC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF84ZTMyNzlhN2QxMDI0NzM1YjcyOTMxNGNmYTViZDFhNS5zZXRDb250ZW50KGh0bWxfNDM5Mjg3NzdiZTk1NGJkY2I5ODdiYjZjYzY1NjhlZDMpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV9lYTE5OWE2MDczNTQ0MTdjOTQzZmJkNzllZjlmNDdkYS5iaW5kUG9wdXAocG9wdXBfOGUzMjc5YTdkMTAyNDczNWI3MjkzMTRjZmE1YmQxYTUpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzZiNzFlOThhN2Q5OTQ1MWE4MjJjZDZlMzdhZmU0MjQ5ID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjQuNzIwODgxOCwgOTMuOTIyOTM4Nl0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDgzNDguMzMzMzMzMzMzMzM0LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfZjE3NmZmOWVhZjQwNDU1Y2JmM2IwNmQ5NjJjOTRlMjQgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfODljNjY1NTQ0MDM4NDIzYjlkMmU0MDQyZTI2Y2Q4YmQgPSAkKGA8ZGl2IGlkPSJodG1sXzg5YzY2NTU0NDAzODQyM2I5ZDJlNDA0MmUyNmNkOGJkIiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5NYW5pcHVyICAyNTA0NSAgb24gMzAvMTEvMjAyMCAyMDozMDoyMDwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfZjE3NmZmOWVhZjQwNDU1Y2JmM2IwNmQ5NjJjOTRlMjQuc2V0Q29udGVudChodG1sXzg5YzY2NTU0NDAzODQyM2I5ZDJlNDA0MmUyNmNkOGJkKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfNmI3MWU5OGE3ZDk5NDUxYTgyMmNkNmUzN2FmZTQyNDkuYmluZFBvcHVwKHBvcHVwX2YxNzZmZjllYWY0MDQ1NWNiZjNiMDZkOTYyYzk0ZTI0KQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV80YzNjMTFhZmQ4ZDc0MGFmYjRkZDkxYTFhNTAyNjg1MiA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzI3LjY4OTE3MTIsIDk2LjQ1OTcyMjZdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA1NDI3LjMzMzMzMzMzMzMzMywKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwX2VhZjFkN2IxZjlkYzQzMTQ5ZTMyMzJmNWEzMTlmNzYwID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzVmZDJkZjY4NWJkNjRlNTU4MmUyNmFkMjU2YTRjNjlhID0gJChgPGRpdiBpZD0iaHRtbF81ZmQyZGY2ODViZDY0ZTU1ODJlMjZhZDI1NmE0YzY5YSIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+QXJ1bmFjaGFsIFByYWRlc2ggIDE2MjgyICBvbiAzMC8xMS8yMDIwIDIzOjI5OjM4PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF9lYWYxZDdiMWY5ZGM0MzE0OWUzMjMyZjVhMzE5Zjc2MC5zZXRDb250ZW50KGh0bWxfNWZkMmRmNjg1YmQ2NGU1NTgyZTI2YWQyNTZhNGM2OWEpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV80YzNjMTFhZmQ4ZDc0MGFmYjRkZDkxYTFhNTAyNjg1Mi5iaW5kUG9wdXAocG9wdXBfZWFmMWQ3YjFmOWRjNDMxNDllMzIzMmY1YTMxOWY3NjApCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlX2QzNzEyZjU3MDMzZDQ5Mzc5NjRmNjFkMGVjZDVlMDRjID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMzAuNzMzNDQyMSwgNzYuNzc5NzE0M10sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDU4MDMuMCwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwX2M4YjAwY2I0MWU1ODRlYjc5YjkzYWU3OTExYzc1NzVjID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzAxZjJmYjAyNWIyNDRhZmI4NjgxMjM4YWRmMmY1MTRiID0gJChgPGRpdiBpZD0iaHRtbF8wMWYyZmIwMjViMjQ0YWZiODY4MTIzOGFkZjJmNTE0YiIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+Q2hhbmRpZ2FyaCAgMTc0MDkgIG9uIDMwLzExLzIwMjAgMjA6MzA6MjU8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwX2M4YjAwY2I0MWU1ODRlYjc5YjkzYWU3OTExYzc1NzVjLnNldENvbnRlbnQoaHRtbF8wMWYyZmIwMjViMjQ0YWZiODY4MTIzOGFkZjJmNTE0Yik7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlX2QzNzEyZjU3MDMzZDQ5Mzc5NjRmNjFkMGVjZDVlMDRjLmJpbmRQb3B1cChwb3B1cF9jOGIwMGNiNDFlNTg0ZWI3OWI5M2FlNzkxMWM3NTc1YykKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKCiAgICAgICAgICAgIHZhciBjaXJjbGVfOWJiZDdlYjhkZjUzNGE3ZWI2MWRiYTczZWQ0NGEyMmIgPSBMLmNpcmNsZSgKICAgICAgICAgICAgICAgIFsyNS41Mzc5NDMyLCA5MS4yOTk5MTAyXSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogInJlZCIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogdHJ1ZSwKICAiZmlsbENvbG9yIjogInJlZCIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogMzk1OC4zMzMzMzMzMzMzMzM1LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfOTBlMjA4ZWQzMzM0NGE4ZjkyOGRkOTlmOTU5ZGE5MTQpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfZmUyM2E2NjZhYzVlNGE3NThjOTE2MTQ1YjZjMGRhNzAgPSBMLnBvcHVwKHttYXhXaWR0aDogJzEwMCUnCiAgICAgICAgICAgIAogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfNjQ1MTg2MmQ4YjY0NGQ2MmFhNmQxMWQyY2I3MDNmMmYgPSAkKGA8ZGl2IGlkPSJodG1sXzY0NTE4NjJkOGI2NDRkNjJhYTZkMTFkMmNiNzAzZjJmIiBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij5NZWdoYWxheWEgIDExODc1ICBvbiAwMS8xMi8yMDIwIDE5OjIxOjQ5PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF9mZTIzYTY2NmFjNWU0YTc1OGM5MTYxNDViNmMwZGE3MC5zZXRDb250ZW50KGh0bWxfNjQ1MTg2MmQ4YjY0NGQ2MmFhNmQxMWQyY2I3MDNmMmYpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV85YmJkN2ViOGRmNTM0YTdlYjYxZGJhNzNlZDQ0YTIyYi5iaW5kUG9wdXAocG9wdXBfZmUyM2E2NjZhYzVlNGE3NThjOTE2MTQ1YjZjMGRhNzApCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzNhYjYwZTRlNDRkYjQzYTFiMjBlMjBlZjE2MWJlNDg3ID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjYuMTYzMDU1NiwgOTQuNTg4NDkxMV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDM3MjguNjY2NjY2NjY2NjY2NSwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzU3YWNkOTE0YTYwMTRlNGJiZmEwM2RhZTVjOTAxN2M3ID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sX2VkZmM5MmJiNTMwMjRmYzA4OTkxMzI1YmNhZjY4Yjk0ID0gJChgPGRpdiBpZD0iaHRtbF9lZGZjOTJiYjUzMDI0ZmMwODk5MTMyNWJjYWY2OGI5NCIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+TmFnYWxhbmQgIDExMTg2ICBvbiAzMC8xMS8yMDIwIDIwOjIwOjU4PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF81N2FjZDkxNGE2MDE0ZTRiYmZhMDNkYWU1YzkwMTdjNy5zZXRDb250ZW50KGh0bWxfZWRmYzkyYmI1MzAyNGZjMDg5OTEzMjViY2FmNjhiOTQpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV8zYWI2MGU0ZTQ0ZGI0M2ExYjIwZTIwZWYxNjFiZTQ4Ny5iaW5kUG9wdXAocG9wdXBfNTdhY2Q5MTRhNjAxNGU0YmJmYTAzZGFlNWM5MDE3YzcpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzI4OWYzYzA0M2RlZjQ4MGRiMzhjNTExZGNlNzNiMzEzID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMzMuOTQ1NjQwNywgNzcuNjU2ODU3Nl0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDI4MDUuMCwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzhmZjFmMGI2ZTE3YjRhMmQ5OGM1OTgzYWFjYjNmM2U0ID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzJhNDFkNWZiOGE1NDQ1NGY4ZTdkZmY3YzQxN2JjYWMwID0gJChgPGRpdiBpZD0iaHRtbF8yYTQxZDVmYjhhNTQ0NTRmOGU3ZGZmN2M0MTdiY2FjMCIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+TGFkYWtoICA4NDE1ICBvbiAzMC8xMS8yMDIwIDIzOjM3OjM1PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF84ZmYxZjBiNmUxN2I0YTJkOThjNTk4M2FhY2IzZjNlNC5zZXRDb250ZW50KGh0bWxfMmE0MWQ1ZmI4YTU0NDU0ZjhlN2RmZjdjNDE3YmNhYzApOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV8yODlmM2MwNDNkZWY0ODBkYjM4YzUxMWRjZTczYjMxMy5iaW5kUG9wdXAocG9wdXBfOGZmMWYwYjZlMTdiNGEyZDk4YzU5ODNhYWNiM2YzZTQpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzg1YTZlMDBkN2NlYzRjNGZiNGE1MWRkODY3ZWM2Zjc5ID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMTAuMjE4ODM0NCwgOTIuNTc3MTMyOV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDE1NzAuMCwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwX2NkYTNlNGYxNTY3YjQ5ZTk4NjI2ZGI4ODQ2MzllZGY5ID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sX2Y0YWI5NDYyOGE4NzRkZGE4ODY5ZjdjMDE5OTIzYzdiID0gJChgPGRpdiBpZD0iaHRtbF9mNGFiOTQ2MjhhODc0ZGRhODg2OWY3YzAxOTkyM2M3YiIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+QW5kYW1hbiBhbmQgTmljb2JhciBJc2xhbmRzICA0NzEwICBvbiAzMC8xMS8yMDIwIDIyOjUyOjQ5PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF9jZGEzZTRmMTU2N2I0OWU5ODYyNmRiODg0NjM5ZWRmOS5zZXRDb250ZW50KGh0bWxfZjRhYjk0NjI4YTg3NGRkYTg4NjlmN2MwMTk5MjNjN2IpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV84NWE2ZTAwZDdjZWM0YzRmYjRhNTFkZDg2N2VjNmY3OS5iaW5kUG9wdXAocG9wdXBfY2RhM2U0ZjE1NjdiNDllOTg2MjZkYjg4NDYzOWVkZjkpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlX2M4M2E3ZGEyNTA5ODQ4NDU4YjdhOTNiMjY2Mjg1OWEwID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjcuNjAxMDI5LCA4OC40NTQxMzYzODY4MDE0NV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDE2NjMuMzMzMzMzMzMzMzMzMywKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzYyY2M0NWJiOWI4NDRiNzJiODZkZmZlODRjMzY3N2M5ID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzFmNDdhYzM2NzNmYTQzYTFhODk3ODk4YjQ5MmI3MGM1ID0gJChgPGRpdiBpZD0iaHRtbF8xZjQ3YWMzNjczZmE0M2ExYTg5Nzg5OGI0OTJiNzBjNSIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+U2lra2ltICA0OTkwICBvbiAzMC8xMS8yMDIwIDIzOjEzOjI3PC9kaXY+YClbMF07CiAgICAgICAgICAgICAgICBwb3B1cF82MmNjNDViYjliODQ0YjcyYjg2ZGZmZTg0YzM2NzdjOS5zZXRDb250ZW50KGh0bWxfMWY0N2FjMzY3M2ZhNDNhMWE4OTc4OThiNDkyYjcwYzUpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIGNpcmNsZV9jODNhN2RhMjUwOTg0ODQ1OGI3YTkzYjI2NjI4NTlhMC5iaW5kUG9wdXAocG9wdXBfNjJjYzQ1YmI5Yjg0NGI3MmI4NmRmZmU4NGMzNjc3YzkpCiAgICAgICAgICAgIDsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgCgogICAgICAgICAgICB2YXIgY2lyY2xlXzU2OGI1ZjliM2VhMjQxMTk5OWNiNmIxZDllNWMxYTMxID0gTC5jaXJjbGUoCiAgICAgICAgICAgICAgICBbMjAuMjczMzYwNCwgNzMuMDA0NDk4OF0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICJyZWQiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IHRydWUsCiAgImZpbGxDb2xvciI6ICJyZWQiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDExMDkuMzMzMzMzMzMzMzMzMywKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwXzkwZTIwOGVkMzMzNDRhOGY5MjhkZDk5Zjk1OWRhOTE0KTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHBvcHVwX2I4MzljM2YxZWZlNTRkMDY4Y2E3OWY3YWE5N2MwMjBiID0gTC5wb3B1cCh7bWF4V2lkdGg6ICcxMDAlJwogICAgICAgICAgICAKICAgICAgICAgICAgfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzk3ZTJlYjY1Y2IwZjRiMGViYmQxYjMxZGY3ZmMxNTQyID0gJChgPGRpdiBpZD0iaHRtbF85N2UyZWI2NWNiMGY0YjBlYmJkMWIzMWRmN2ZjMTU0MiIgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+RGFkcmEgYW5kIE5hZ2FyIEhhdmVsaSBhbmQgRGFtYW4gYW5kIERpdSAgMzMyOCAgb24gMDEvMTIvMjAyMCAxNjozMDo0NTwvZGl2PmApWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfYjgzOWMzZjFlZmU1NGQwNjhjYTc5ZjdhYTk3YzAyMGIuc2V0Q29udGVudChodG1sXzk3ZTJlYjY1Y2IwZjRiMGViYmQxYjMxZGY3ZmMxNTQyKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBjaXJjbGVfNTY4YjVmOWIzZWEyNDExOTk5Y2I2YjFkOWU1YzFhMzEuYmluZFBvcHVwKHBvcHVwX2I4MzljM2YxZWZlNTRkMDY4Y2E3OWY3YWE5N2MwMjBiKQogICAgICAgICAgICA7CgogICAgICAgICAgICAKICAgICAgICAKICAgIAoKICAgICAgICAgICAgdmFyIGNpcmNsZV80NjUxNmYxMTA2ZGE0YzFiOTJmNTgzNzBhMTI5NGE4OSA9IEwuY2lyY2xlKAogICAgICAgICAgICAgICAgWzIzLjIxNDYxNjksIDkyLjg2ODc2MTJdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAicmVkIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiB0cnVlLAogICJmaWxsQ29sb3IiOiAicmVkIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiAxMjgyLjMzMzMzMzMzMzMzMzMsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF85MGUyMDhlZDMzMzQ0YThmOTI4ZGQ5OWY5NTlkYTkxNCk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBwb3B1cF84ZDM1MGIzMmJkZmY0NzhjYmJlZGQyYTI3MjZmNjIwMyA9IEwucG9wdXAoe21heFdpZHRoOiAnMTAwJScKICAgICAgICAgICAgCiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF8yYjE0MmNiMTZkNjc0NGUyYmJkM2Y0YTk1NTVhNmU1MyA9ICQoYDxkaXYgaWQ9Imh0bWxfMmIxNDJjYjE2ZDY3NDRlMmJiZDNmNGE5NTU1YTZlNTMiIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPk1pem9yYW0gIDM4NDcgIG9uIDAxLzEyLzIwMjAgMTk6MjE6MDg8L2Rpdj5gKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzhkMzUwYjMyYmRmZjQ3OGNiYmVkZDJhMjcyNmY2MjAzLnNldENvbnRlbnQoaHRtbF8yYjE0MmNiMTZkNjc0NGUyYmJkM2Y0YTk1NTVhNmU1Myk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgY2lyY2xlXzQ2NTE2ZjExMDZkYTRjMWI5MmY1ODM3MGExMjk0YTg5LmJpbmRQb3B1cChwb3B1cF84ZDM1MGIzMmJkZmY0NzhjYmJlZGQyYTI3MjZmNjIwMykKICAgICAgICAgICAgOwoKICAgICAgICAgICAgCiAgICAgICAgCjwvc2NyaXB0Pg== onload=\"this.contentDocument.open();this.contentDocument.write(atob(this.getAttribute('data-html')));this.contentDocument.close();\" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>"
            ],
            "text/plain": [
              "<folium.folium.Map at 0x7ff5f713ff98>"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 5
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Pcb7pRe5eeJJ"
      },
      "source": [
        "**Note:** The `folium_map_with_circles()` function is NOT a standard Python function. It is a user-defined function created at WhiteHat Jr using Python to simplify the map creation process. You will learn to create your own user-defined function in the subsequent classes in this course.\n",
        "\n",
        "Let's export the above map as an HTML file. You can make it a web page like a website and share it with your parents or friends. To do this, you need to use the `save()` function which is a standard Python function. The input to this function should be a path (or location) of the directory where you want to store the HTML file. Also, name the file as `index.html`. This is very important."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0Y1VFs1vWcL2",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 197
        },
        "outputId": "18e85f80-6241-4ce2-e4ce-f15782c95be5"
      },
      "source": [
        "# Student Action: Export the world map as an HTML file.\n",
        "india_map=folium_map_with_circles(\"hemanth\",\"India\",700,500,1,4,'Stamen Toner',3,'red',True)\n",
        "india_map.save('/content/index.html') \n"
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "error",
          "ename": "NameError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-f51507a2af87>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;31m# Student Action: Export the world map as an HTML file.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0mindia_map\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mfolium_map_with_circles\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"hemanth\"\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\"India\"\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;36m700\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;36m500\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;36m1\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;36m4\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m'Stamen Toner'\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;36m3\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m'red'\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m \u001b[0mindia_map\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msave\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'/content/index.html'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mNameError\u001b[0m: name 'folium_map_with_circles' is not defined"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XQS9oIkAFw6u"
      },
      "source": [
        "---"
      ]
    }
  ]
}