#Programm qui permet d'utiliser l'interface graphique Tkinter pour recevoir des suggestions de musées ou de festivals.

import sys
import os.path
from pathlib import Path 

scriptpath = str(os.path.dirname(os.path.abspath(__file__)))
scriptpath_parent = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

sys.path.insert(0, scriptpath_parent)

from geolocalisation import find_museums
from data_extraction import festival_dpt

import re
from PIL import ImageTk, Image
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from tkinter import messagebox

class application(ttk.Notebook):
    
    """
        this is will serve to make the Graphical Interface
    """

    def __init__(self, stat_show, master):
        ttk.Notebook.__init__(self, master)
        self.stat_show = stat_show
        self.master = master
        self.customize_window()
        self.grid()
        self.create_museums_tab_widgets()
        self.create_festivals_tab_widgets()
        if self.stat_show:
            self.create_statistics_tab_widgets()
    
    def customize_window(self):

        style = ttk.Style()

        style.theme_create( "yummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": 'white'} },
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": 'medium sea green', 'foreground':'white', 'font':'Lora 13'},
                "map":       {"background": [("selected", 'medium sea green')],
                              "expand": [("selected", [1, 1, 1, 0])] } } } )

        style.theme_use("yummy")
        
        self.master.resizable(width = False, height = False)
        self.master.title("FindMeCulture")
        self.master.geometry('1420x650')
        icon_dir = str(os.path.join(scriptpath,"museum_icon.ico"))
        self.master.iconbitmap(icon_dir)
        self.master.configure(background='medium sea green')

        self.museums_tab = tk.Frame(self, bg='medium sea green')
        self.add(self.museums_tab, text="Museums")
        self.festivals_tab = tk.Frame(self, bg='medium sea green')
        self.add(self.festivals_tab, text='Festivals')
        self.statistics_tab = tk.Frame(self, bg='white')
        if self.stat_show:
            self.add(self.statistics_tab, text='Statistics')
        self.grid()
    
    @staticmethod
    def adjust_column_width(frame, width):
        for i in range(width+1):
            frame.grid_columnconfigure(i, weight=2)
    
    @staticmethod
    def adjust_row_height(frame, height):
        for i in range(height+1):
            frame.grid_rowconfigure(i, weight=1)

################################################################### start of [museums_tab] part of the code #############################################################################    def create_museums_tab_widgets(self):
    
    def create_museums_tab_widgets(self):
        self.adjust_column_width(self.museums_tab, 7)
        self.adjust_row_height(self.museums_tab, 7)
        self.create_adress_line()
        self.create_ville_line()
        self.create_num_museum_line()
        self.create_max_distance_line()
        self.create_output_zone()
        self.create_submit_button()
        self.create_clear_button()
        self.create_clear_fields_button()
        
    def create_adress_line(self):
        adress_label = tk.Label(self.museums_tab, text="Adresse: ", fg="White", font=("Lora", 14))
        adress_label.configure(background='medium sea green')
        adress_label.grid(row=1, column=0)
        self.adress_entry = tk.Entry(self.museums_tab, width=90, font=("Lora", 14))
        self.adress_entry.grid(row=1, column=1, columnspan=2)

    def create_ville_line(self):
        ville_label = tk.Label(self.museums_tab, text="Ville: ", fg="White", font=("Lora", 14))
        ville_label.configure(background='medium sea green')
        ville_label.grid(row=2, column=0)
        self.ville_entry = tk.Entry(self.museums_tab, width=90, font=("Lora", 14))
        self.ville_entry.grid(row=2, column=1, columnspan=2)

    def create_num_museum_line(self):
        num_museum_label = tk.Label(self.museums_tab, text="Nombre de musées à afficher: ", fg="White", font=("Lora", 14))
        num_museum_label.configure(background="medium sea green")
        num_museum_label.grid(row=3, column=0)
        self.num_museum_entry = tk.Entry(self.museums_tab, width=90, font=("Lora", 14))
        self.num_museum_entry.grid(row=3, column=1, columnspan=2)

    def create_max_distance_line(self):
        max_distance_label = tk.Label(self.museums_tab, text="Distance maximale (km): ", fg="White", font=("Lora", 14))
        max_distance_label.configure(background="medium sea green")
        max_distance_label.grid(row=4, column=0)
        self.max_distance_entry = tk.Entry(self.museums_tab, width=90, font=("Lora", 14))
        self.max_distance_entry.grid(row=4, column=1, columnspan=2)

    def create_submit_button(self):
        self.submit_button = tk.Button(self.museums_tab, bg="white", text="Submit", font=("Lora", 12), relief=tk.FLAT, command=lambda:self.submit_command())
        self.submit_button.configure(width=20)
        self.submit_button.grid(row=5, column=0)

    def create_clear_fields_button(self):
        self.clear_field_button = tk.Button(self.museums_tab, bg="white", text="Clear fields", font=("Lora", 12), relief=tk.FLAT, command=lambda:self.clear_field_button_command())
        self.clear_field_button.configure(width=20)
        self.clear_field_button.grid(row=5, column=1)

    def create_clear_button(self):
        self.clear_results_button = tk.Button(self.museums_tab, bg="white", text="Clear results", font=("Lora", 12), relief=tk.FLAT, command=lambda:self.clear_output_zone_command())
        self.clear_results_button.configure(width=20)
        self.clear_results_button.grid(row=5, column=2)

    def create_output_zone(self):
        self.output_zone = ScrolledText(self.museums_tab, height=18, width=126, font=("Lora", 14))
        self.output_zone.grid(row=6, column=0, columnspan=3)
        self.output_zone.insert(1.0, "Le résultat s'affichera ici: ")

    # Les commandes des boutons : {
    def show_text_in_output_zone(self, text_to_show):
        self.output_zone.insert(tk.END, '\n')
        self.output_zone.insert(tk.END, text_to_show)
    
    def submit_command(self):
        adress_value = self.adress_entry.get()
        ville_value = self.ville_entry.get()
        num_museum_value = self.num_museum_entry.get()
        max_distance_value = self.max_distance_entry.get()
        if len(adress_value)==0 or len(ville_value)==0 or len(max_distance_value)==0 or len(num_museum_value)==0:
            messagebox.showerror("Error", "Tous les champs doivent être remplis")
        else:
            self.output_zone.delete(1.0, tk.END)
            museums = find_museums.find_nearest_museums(adress_value, ville_value, max_distance=int(max_distance_value), num_museums=int(num_museum_value))
            not_empty = False
            num_museums_found = 0
            
            for pos, museum in museums:
                not_empty = True
                text = find_museums.text_to_show_for_museum(museum, pos)
                self.show_text_in_output_zone(text)
                num_museums_found += 1

            if not(not_empty):
                #if the list of results is empty, then we have no results to show
                messagebox.showinfo("Internal Error", "Pas de résultats")
            
            self.output_zone.insert(1.0, "On a trouvé {} musées:".format(num_museums_found))

    def clear_field_button_command(self):
        self.adress_entry.delete(0, tk.END)
        self.ville_entry.delete(0, tk.END)
        self.num_museum_entry.delete(0, tk.END)
        self.max_distance_entry.delete(0, tk.END)
    
    def clear_output_zone_command(self):
            self.output_zone.delete(1.0, tk.END)
            self.output_zone.insert(1.0, "Le résultat s'affichera ici: ")
    # }

################################################################### end of [museums_tab] part of the code #############################################################################

############################################################### start of the [festivals_tab] part of the code #########################################################################
    
    def create_festivals_tab_widgets(self):
        self.adjust_column_width(self.festivals_tab, 7)
        self.adjust_row_height(self.festivals_tab, 7)
        self.create_dep_line()
        self.create_domaine_line()
        self.create_festivals_output_zone()
        self.create_festival_submit_button()
        self.create_festival_clear_fields_button()
        self.create_festival_clear_results_button()
    
    def create_dep_line(self):
        dep_label = tk.Label(self.festivals_tab, text="Choisir le département: ", fg="White", font=("Lora", 14))
        dep_label.configure(background="medium sea green")
        dep_label.grid(row=0, column=0)
        self.dep_combobox = ttk.Combobox(self.festivals_tab, postcommand=self.on_dep_postcommand, font='Lora 14', width=90)
        self.dep_combobox.grid(row=0, column=1, columnspan=2)

    def create_domaine_line(self):
        domaine_label = tk.Label(self.festivals_tab, text="Choisir le domaine: ", fg="White", font=("Lora", 14))
        domaine_label.configure(background="medium sea green")
        domaine_label.grid(row=1, column=0)
        self.domaine_combobox = ttk.Combobox(self.festivals_tab, postcommand=self.on_domaine_postcommand, font="Lora 14", width=90)
        self.domaine_combobox.grid(row=1, column=1, columnspan=2)  

    def create_festival_submit_button(self):
        self.festival_submit_button = tk.Button(self.festivals_tab, bg="white", text="Submit", font=("Lora", 12), relief=tk.FLAT, command=lambda:self.festival_submit_button_command())
        self.festival_submit_button.configure(width=20)
        self.festival_submit_button.grid(row=2, column=0)

    def create_festival_clear_fields_button(self):
        self.festival_clear_fields_button = tk.Button(self.festivals_tab, bg="white", text="Clear fields", font=("Lora", 12), relief=tk.FLAT, command=lambda:self.festival_clear_fields_command())
        self.festival_clear_fields_button.configure(width=20)
        self.festival_clear_fields_button.grid(row=2, column=1)

    def create_festival_clear_results_button(self):
        self.festival_clear_results_button = tk.Button(self.festivals_tab, bg="white", text="Clear results", font=("Lora", 12), relief=tk.FLAT, command=lambda:self.festival_clear_results_command())
        self.festival_clear_results_button.configure(width=20)
        self.festival_clear_results_button.grid(row=2, column=2)

    def create_festivals_output_zone(self):
        self.festival_output_zone = ScrolledText(self.festivals_tab, height=23, width=126, font=("Lora", 14))
        self.festival_output_zone.grid(row=4, column=0, columnspan=3)
        self.festival_output_zone.insert(1.0, "Le résultat s'affichera ici: ")    

# festival commands : {
    def show_festival_text_in_output_zone(self, text_to_show):
        self.festival_output_zone.insert(tk.END, '\n')
        self.festival_output_zone.insert(tk.END, text_to_show)
    
    def on_dep_postcommand(self):
        
        initial_dep_options = festival_dpt.DEPARTMENTS.values()
        dep_combobox_value = self.dep_combobox.get()
        
        #pattern to match written text to any region with no case sensitivity
        dep_combobox_value_pattern = ''.join('[' + letter.upper() + letter.lower() + ']' for letter in dep_combobox_value) 
        pattern = '^' + dep_combobox_value_pattern + '.*'
        
        suggestion_list_dep = [] 
        
        for item in initial_dep_options:
            if re.match(pattern, item) is not None:
                suggestion_list_dep.append(item)
        
        if len(suggestion_list_dep)==0:
            suggestion_list_dep.append('Pas de résultats')
        
        self.dep_combobox['values'] = suggestion_list_dep


    def on_domaine_postcommand(self):
        if len(self.dep_combobox.get()) > 0:
            initial_domaine_options = festival_dpt.liste_domaine_festival_departement(self.dep_combobox.get())
            domain_combobox_value = self.domaine_combobox.get()
            
            #pattern to match written text to any region with no case sensitivity
            domain_combobox_value_pattern = ''.join('[' + letter.upper() + letter.lower() + ']' for letter in domain_combobox_value)
            pattern = '^' + domain_combobox_value_pattern + '.*'
            
            suggestion_list_domaine = [] 
            
            for item in initial_domaine_options:
                if re.match(pattern, item) is not None:
                    suggestion_list_domaine.append(item)
            
            if len(suggestion_list_domaine)==0:
                suggestion_list_domaine.append('Pas de résultats')
            
            self.domaine_combobox['values'] = suggestion_list_domaine

        #catch an eventual case where the department isn't specified on domaine postcommand
        else:
            self.domaine_combobox['values'] = ['Pas de résultats']

    def festival_submit_button_command(self):
        self.clear_output_zone_command()
        domaine_value = self.domaine_combobox.get()
        dep_value = self.dep_combobox.get()
        if len(dep_value)==0:
            messagebox.showerror('Error', 'Au moins le champ "Département" doit être remplis !')
        elif len(domaine_value)==0:
            self.festival_output_zone.delete(1.0, tk.END)
            try:
                festival_to_show_list = festival_dpt.get_festivals_for_departement(dep_value)
                if len(festival_to_show_list) == 0:
                    messagebox.showinfo('Internal Error', 'Pas de résultats')
                else:
                    for pos, festival in enumerate(festival_to_show_list):
                        text_to_show = festival_dpt.make_festival_text(festival, pos)
                        self.show_festival_text_in_output_zone(text_to_show)
            except:
                messagebox.showinfo('Internal Error', 'Pas de résultats')
        else:
            try:
                self.festival_output_zone.delete(1.0, tk.END)
                festival_to_show_list = festival_dpt.liste_domaine_festival_departement(dep_value, domaine=domaine_value)
                if len(festival_to_show_list) == 0:
                    messagebox.showinfo('Internal Error', 'Pas de résultats')
                else:
                    for pos, festival in enumerate(festival_to_show_list):
                        text_to_show = festival_dpt.make_festival_text(festival, pos)
                        self.show_festival_text_in_output_zone(text_to_show)
            except:
                messagebox.showinfo('Internal Error', 'Pas de résultats')

    
    def festival_clear_fields_command(self):
        self.dep_combobox.delete(0, tk.END)
        self.domaine_combobox.delete(0, tk.END)

    def festival_clear_results_command(self):
        self.festival_output_zone.delete(1.0, tk.END)
        self.festival_output_zone.insert(1.0, "Le résultat s'affichera ici: ")
#}

################################################################## end of [festivals_tab] part of the code #############################################################################

################################################################ start of [statistics_tab] part of the code ############################################################################

    def create_statistics_tab_widgets(self):
        self.adjust_column_width(self.statistics_tab, 7)
        self.adjust_row_height(self.statistics_tab, 7)
        self.create_diagrams_line()

    def create_diagrams_line(self):
        diagrams_label = tk.Label(self.statistics_tab, text="Choisir le graphe: ", bg='medium sea green', fg="white", font=("Lora", 12))
        diagrams_label.grid(row=0, column=0)
        self.diagrams_combobox = ttk.Combobox(self.statistics_tab, font="Lora 14", postcommand=self.graphs_on_post_command, width=70)
        self.diagrams_combobox.grid(row=0, column=3)
        self.diagrams_show_button = tk.Button(self.statistics_tab, text='Show', width=10, font="Lora 10", bg='medium sea green', relief=tk.FLAT, command=lambda:self.statistics_diagrams_show_command())
        self.diagrams_show_button.grid(row=0, column=5)
        blank_path = os.path.join(scriptpath_parent, r'graphes', r'blank.png')
        blank_image = ImageTk.PhotoImage(Image.open(blank_path))
        self.image_placing = tk.Label(self.statistics_tab, image=blank_image, border=0, bg='white')
        self.image_placing.grid(row=4, column=3)

    def graphs_on_post_command(self):
        image_dir = os.path.join(scriptpath_parent, r'graphes')
        image_list = os.listdir(image_dir)
        image_list = [ image.split('.')[0] for image in image_list if 'blank' not in image ]
        self.diagrams_combobox['values'] = image_list

    def statistics_diagrams_show_command(self):
        self.image_placing.grid_remove()
        graph_name = self.diagrams_combobox.get()
        graph_path = os.path.join(scriptpath_parent, r'graphes', graph_name + '.png')
        graph_image = ImageTk.PhotoImage(Image.open(graph_path))
        self.image_placing.configure(image=graph_image, border=0)
        self.image_placing.img = graph_image
        self.image_placing.grid(row=4, column=3)
        
################################################################## end of [festivals_tab] part of the code #############################################################################

#fonction pour execution
def run_app(stat_show=True):
    root = tk.Tk()
    application(stat_show, root)
    root.mainloop()
