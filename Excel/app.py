import re
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from pandas.errors import ParserError
import tkinter.simpledialog as dialog
from extractor import Extractor

class FiledialogFrame(tk.Frame):
    
    def __init__(self,master,*,label_text:str,button_text:str,button_comand):
        super().__init__(master)
        self.label = tk.Label(self,text=label_text)
        self.button = tk.Button(self,text=button_text,command=button_comand)
        
        self.columnconfigure([0,1], weight=1)
        self.label.grid(row=0,column=0, padx=5,pady=5, sticky='w')
        self.button.grid(row=0,column=1, padx=5,pady=5,sticky='e')

class TemplateFrame(tk.Frame):
    
    def __init__(self,master,*,label_text:str,combobox_var:tk.StringVar,combobox_values:list[str],combobox_bind):
        super().__init__(master)
        self.label = tk.Label(self,text=label_text)
        self.combobox = ttk.Combobox(self,textvariable=combobox_var,values=combobox_values,state='readonly')
        self.combobox.bind('<<ComboboxSelected>>',combobox_bind)
        self.combobox.current(0)
        
        self.columnconfigure(1,weight=1)
        self.label.grid(row=0,column=0,padx=5,sticky='w')
        self.combobox.grid(row=0,column=1,padx=5,sticky='ew')

class SheetFrame(tk.Frame):

    def __init__(self,master,*,label_text:str,spinbox_var):
        super().__init__(master)
        self.label = tk.Label(self, text=label_text)
        self.spinnbox = tk.Spinbox(self, from_=1,to=255,textvariable=spinbox_var,wrap=True,state='readonly',width=5)
        
        self.label.grid(row=0,column=0,padx=5)
        self.spinnbox.grid(row=0,column=1,padx=5)

class RangeFrame(tk.Frame):
    
    def __init__(self,master,*,label_text:str,range_var:tk.StringVar,entry_validate,):
        super().__init__(master)
        self.label = tk.Label(self, text=label_text)
        self.entry_range = tk.Entry(self, textvariable=range_var, validate="key", validatecommand=entry_validate)
        
        self.columnconfigure(1, weight=1)
        self.label.grid(row=0,column=0,padx=5,pady=5,sticky='w')
        self.entry_range.grid(row=0,column=1,padx=5,pady=5,sticky='ew')
        
class InfoFrame(tk.Frame):
    
    def __init__(self, master,*,info_var:tk.StringVar):
        super().__init__(master)
        self.entry = tk.Entry(self, textvariable=info_var, state='readonly',bd=0,foreground='gray',readonlybackground='white')
        self.scrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.entry.xview, style='arrowless.Horizontal.TScrollbar')
        self.entry.config(xscrollcommand=self.scrollbar.set)
        
        self.columnconfigure(0,weight=1)
        self.entry.grid(row=0,padx=5,sticky='ew')
        self.scrollbar.grid(row=1,padx=5,sticky='ew')

class ColumnsFrame(tk.Frame):
    
    def __init__(self,master,col_count:int,old_column_names:list[str],new_column_names:list[tk.StringVar],columns_to_keep:list[tk.IntVar]):
        super().__init__(master)
        self.label1 = tk.Label(self,text='Nazwa kolumny:')
        self.label2 = tk.Label(self,text='Nowa nazwa:')
        self.label3 = tk.Label(self,text='Zachowaj kolumnę:')
        
        self.inner = tk.Frame(self)
        cnv_canvas = tk.Canvas(self.inner,height=72,width=550,highlightthickness=0)
        frm_canvas = tk.Frame(cnv_canvas)
        
        for i in range(col_count):
            frm_canvas.columnconfigure(i,weight=1)
            lbl_canvas = tk.Label(frm_canvas,text=old_column_names[i])
            lbl_canvas.grid(row=0,column=i,padx=5,pady=2,sticky='ew')
            ent_canvas = tk.Entry(frm_canvas,textvariable=new_column_names[i],takefocus=False)
            ent_canvas.grid(row=1,column=i,padx=5,pady=2,sticky='ew')
            chk_canvas = ttk.Checkbutton(frm_canvas,variable=columns_to_keep[i],onvalue = 1, offvalue = 0,takefocus=False)
            chk_canvas.grid(row=2,column=i,padx=5,pady=2)
            
        win_canvas = cnv_canvas.create_window((0,0),window=frm_canvas, anchor='nw')
        cnv_canvas.pack(fill=tk.X)
            
        scr_scroll = ttk.Scrollbar(self, command=cnv_canvas.xview, orient='horizontal')
        cnv_canvas.config(xscrollcommand=scr_scroll.set)
        frm_canvas.bind('<Configure>',lambda event: cnv_canvas.config(scrollregion=cnv_canvas.bbox('all')))
        cnv_canvas.bind('<Configure>',lambda event: cnv_canvas.itemconfig(win_canvas,height=event.height))
        
        scr_scroll.grid(row=3,column=1,padx=5,sticky='ew')
        
        self.columnconfigure(1,weight=1)
        self.label1.grid(row=0,column=0,padx=5,pady=2,sticky='w')
        self.label2.grid(row=1,column=0,padx=5,pady=2,sticky='w')
        self.label3.grid(row=2,column=0,padx=5,pady=2,sticky='w')
        self.inner.grid(row=0,column=1,rowspan=3,padx=5,sticky='ew')

class FilenameFrame(tk.Frame):
    
    def __init__(self,master,*,label_text:str,entry_var:tk.StringVar,entry_validate):
        super().__init__(master)
        self.label = tk.Label(self, text=label_text)
        self.entry_file = tk.Entry(self, textvariable=entry_var, validate="key", validatecommand=entry_validate)
        self.xslx = tk.Label(self, text='.xlsx')
        
        self.columnconfigure(0, weight=1)
        self.label.grid(row=0,column=0,columnspan=2,padx=5,sticky='w')
        self.entry_file.grid(row=1,column=0,padx=5,sticky='ew')
        self.xslx.grid(row=1,column=1,padx=5,sticky='w')


class Screen1:
    
    def __init__(self, window: tk.Tk, extractor: Extractor):
        self.window = window
        self.ext = extractor
        self.on_load = None
        self.str_size = tk.StringVar(value='Tabela ma wymiary 2x2')
        self.button = tk.Button(self.window,text='Załaduj plik',command=self.load_file,state='disabled')
        
        self.source_f = FiledialogFrame(self.window, label_text='Plik źródłowy:', button_text='Wybierz plik',
                                        button_comand=self.select_source)
        
        self.file_info_f = InfoFrame(self.window, info_var=self.ext.source_var)
        
        self.template_f = TemplateFrame(self.window, label_text='Użyj wzorca (opcjonalne):', combobox_var=self.ext.template_var,
                                        combobox_values=['---',*self.ext.get_template_names()],
                                        combobox_bind=lambda event: self.select_template())
        
        self.sheet_f = SheetFrame(self.window, label_text='Numer arkusza:', spinbox_var=self.ext.sheet_val)
        
        self.range_f = RangeFrame(self.window,label_text='Komórki w których znajduje się tabela (z nagłówkami):',
                                range_var=self.ext.range_var, entry_validate=(self.window.register(self.validate_range), '%P'))
        
        self.info_f = InfoFrame(self.window,info_var=self.str_size)
        
    def select_source(self):
        self.ext.select_source()
        if self.ext.source_ready:
            self.button['state'] = 'normal'
            
    def select_template(self):
        self.ext.select_template()
        self.template_f.focus_set()
        if self.ext.current_template is not None:
            self.validate_range(self.ext.current_template['xl_range'])
        
    def pack_screen(self):
        self.source_f.pack(padx=5,fill=tk.X)
        self.file_info_f.pack(padx=5,fill=tk.X)
        self.template_f.pack(padx=5,fill=tk.X)
        self.sheet_f.pack(padx=5,fill=tk.X)
        self.range_f.pack(padx=5,fill=tk.X)
        self.info_f.pack(padx=5,fill=tk.X)
        self.button.pack(padx=5,pady=5)
        self.window.update()
        self.window.minsize(self.window.winfo_width(),self.window.winfo_height())

    def forget_self(self):
        self.source_f.pack_forget()
        self.file_info_f.pack_forget()
        self.template_f.pack_forget()
        self.sheet_f.pack_forget()
        self.range_f.pack_forget()
        self.info_f.pack_forget()
        self.button.pack_forget()
            
    def load_file(self):
        try:
            self.ext.load_file()
        except ParserError:
            messagebox.showerror(title='Error', message='Podany zasięg nie obejmuje poprawnie tabeli!')
            return
        except ValueError:
            messagebox.showerror(title='Error', message='Arkusz o takim numerze nie istnieje!')
            return
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='Plik o takiej nazwie nie istnieje!')
            return
        except:
            messagebox.showerror(title='Error', message='Nie udało się załadować pliku, sprawdź czy wprowadzone dane są poprawne.')
            return
        self.ext.reposition_templates()
        self.forget_self()
        self.next = Screen2(self.window,self.ext)
        self.next.pack_frames()

    def validate_range(self,xl_range:str):
        xl_range = xl_range.upper()
        x = re.search(r'^[A-Z]+[1-9]\d*:[A-Z]+[1-9]\d*$',xl_range)
        if x is None:
            valid = False
        else:
            match = re.match(r'^([A-Z]+)([1-9]\d*):([A-Z]+)([1-9]\d*)$', xl_range)
            start_column = match.group(1)
            start_row = int(match.group(2))
            end_column = match.group(3)
            end_row = int(match.group(4))

            if start_row >= end_row or len(start_column) > len(end_column) or (len(start_column) == len(end_column) and start_column > end_column):
                valid = False
            else:
                valid = True

        if valid:
            start_index = 0
            for char in start_column:
                start_index = start_index * 26 + (ord(char.upper()) - ord('A')) + 1
            end_index = 0
            for char in end_column:
                end_index = end_index * 26 + (ord(char.upper()) - ord('A')) + 1
            cols = end_index - start_index + 1
            rows = end_row - start_row + 1
            self.str_size.set(f'Tabela ma wymiary {cols}x{rows}')
            self.ext.column_range = f'{start_column}:{end_column}'
            self.ext.column_count = cols
            self.ext.row_skip_count = start_row - 1
            self.ext.row_count = rows - 1
            self.ext.range_ready = True
        else:
            self.str_size.set('Niepoprawny zasięg!')
            self.ext.range_ready = False

        self.button['state'] = 'normal' if self.ext.range_ready and self.ext.source_ready else 'disabled'

        return True

class Screen2:
    
    def __init__(self, window: tk.Tk, extractor: Extractor):
        self.window: tk.Tk = window
        self.ext: Extractor = extractor
        self.frames: dict[str,tk.Frame] = dict()
        self.valid_var = tk.StringVar(value=f'Plik zostanie zapisany jako {self.ext.dst_file_var.get()}.xlsx')
        
        frm_save = tk.Frame(self.window)
        frm_save.columnconfigure([0,1], weight=1)
        self.save_btn = tk.Button(frm_save,text='Zapisz plik', state='disabled', command=self.save_file)
        self.save_btn.grid(row=0,column=0,padx=5,pady=5,sticky='w')
        self.template_btn = tk.Button(frm_save, text='Zapamiętaj wzorzec', state='disabled', command=self.save_template)
        if self.ext.current_template is None:
            self.template_btn['state'] = 'normal'
        self.template_btn.grid(row=0,column=1,padx=5,pady=5,sticky='e')
        
        self.frames['col'] = ColumnsFrame(self.window,col_count=self.ext.column_count,
                                          old_column_names=self.ext.old_column_names,
                                          new_column_names=self.ext.new_column_names,
                                          columns_to_keep=self.ext.columns_to_keep
                                          )
        
        self.frames['fd'] = FiledialogFrame(self.window, label_text='Folder docelowy:', button_text='Wybierz folder',
                                            button_comand=self.select_destination)
        
        self.frames['finfo'] = InfoFrame(self.window,info_var=self.ext.dst_folder_var)

        self.frames['dst'] = FilenameFrame(self.window,label_text='Nazwa pliku docelowego:',entry_var=self.ext.dst_file_var,
                                           entry_validate=(self.window.register(self.validate_filename), '%P'))
        
        self.frames['info'] = InfoFrame(self.window,info_var=self.valid_var)
        
        self.frames['save'] = frm_save
        
    def select_destination(self):
        self.ext.select_destination()
        if self.ext.dst_folder_ready:
            self.save_btn['state'] = 'normal'
            
    def pack_frames(self):
        for frame in self.frames.values():
            frame.pack(padx=5,fill=tk.X)
        self.window.geometry("")
        self.window.update()
        self.window.minsize(self.window.winfo_width(),self.window.winfo_height())

    def forget_frames(self):
        for frame in self.frames.values():
            frame.pack_forget()
            
    def save_file(self):
        try:
            self.ext.save_file()
        except PermissionError:
            messagebox.showerror(title='Error', message='Nie można nadpisać pliku, który jest aktualnie otwarty!')
            return
        except:
            messagebox.showerror(title='Error', message='Nie udało się zapisać pliku, sprawdź czy wprowadzone dane są poprawne.')
            return
        
        self.window.destroy()
        
    def save_template(self):
        name = dialog.askstring(title='Zapamiętaj wzorzec',prompt='Podaj nazwę dla wzorca :')
        if name is not None:
            while name in self.ext.get_template_names():
                name = dialog.askstring(title='Zapamiętaj wzorzec',prompt='Istnieje już wzorzec o tej nazwie.\nPodaj inną nazwę dla wzorca:')
                if name is None:
                    return
            self.ext.save_template(name)
            
    def validate_filename(self, filename: str):
        x = re.search(r'^[-a-zA-Z0-9_ ]+$',filename)
        if x is None:
            self.ext.dst_file_ready = False
            self.valid_var.set('Niepoprawna nazwa pliku!')
        else:
            self.ext.dst_file_ready = True
            self.valid_var.set(f'Plik zostanie zapisany jako {x.group()}.xlsx')

        self.save_btn['state'] = 'normal' if self.ext.dst_folder_ready and self.ext.dst_file_ready else 'disabled'
        self.template_btn['state'] = 'normal' if self.ext.current_template is None and self.ext.dst_file_ready else 'disabled'
        return True


def main():
    window = tk.Tk()

    # poziomy scrollbar bez strzałek
    style = ttk.Style()
    style.layout('arrowless.Horizontal.TScrollbar',
             [('Horizontal.Scrollbar.trough',
               {'sticky': 'we',
                'children': [('Horizontal.Scrollbar.thumb',
                              {'sticky': 'nswe',
                               'unit': '1',
                               'children': [('Horizontal.Scrollbar.grip', {'sticky': ''} )]
                               }
                            )]
                }
               )]
             )

    ext = Extractor(window)
    
    scr1 = Screen1(window,ext)
    scr1.pack_screen()

    window.mainloop()
    
if __name__ == '__main__':
    main()