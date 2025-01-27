import gradio as gr

def link_to_tab1():
    return gr.update(selected='Tab 1')

def link_to_tab2():
    return gr.update(selected='Tab 2')

def link_to_tab3():
    return gr.update(selected='Tab 3')

with gr.Blocks() as demo:
    with gr.Tabs() as tabs:
        with gr.TabItem("Tab 1"):
            gr.Markdown("Witaj w zakładce 1")
        with gr.TabItem("Tab 2"):
            gr.Markdown("Witaj w zakładce 2")
        with gr.TabItem("Tab 3"):
            gr.Markdown("Witaj w zakładce 3")

    with gr.Row():
        gr.Image('1-png.png')
        gr.Button("Przejdź do Zakładki 1").click(link_to_tab1)
    with gr.Row():
        gr.Image('2-png.png')
        gr.Button("Przejdź do Zakładki 2").click(link_to_tab2)
    with gr.Row():
        gr.Image('3-png.png')
        gr.Button("Przejdź do Zakładki 3").click(link_to_tab3)

demo.launch()