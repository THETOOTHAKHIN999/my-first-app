from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp


class BMIApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(8)
        )

        title = MDLabel(
            text="BMI Calculator",
            halign="center",
            size_hint_y=None,
            height=dp(50)
        )

        # Weight input
        self.weight_input = TextInput(
            hint_text="Weight (kg)",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(45)
        )

        # Height input
        self.height_input = TextInput(
            hint_text="Height (cm)",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(45)
        )

        # ဘယ် field ကို keypad ထည့်မလဲ သတ်မှတ်ခြင်း
        self.active_input = self.weight_input

        self.weight_input.bind(
            focus=self.set_active_weight
        )

        self.height_input.bind(
            focus=self.set_active_height
        )

        # Calculator keypad
        keypad = GridLayout(
            cols=3,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(210)
        )

        keypad_buttons = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            ".", "0", "⌫",
            "C", "", ""
        ]

        for key in keypad_buttons:
            if key == "":
                empty_button = Button(
                    text="",
                    disabled=True
                )
                keypad.add_widget(empty_button)
            else:
                button = Button(
                    text=key,
                    font_size=dp(20)
                )
                button.bind(
                    on_release=self.keypad_pressed
                )
                keypad.add_widget(button)

        # Main buttons
        button_row = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        calculate_button = Button(
            text="Calculate",
            background_color=(0, 0.5, 0.5, 1)
        )
        calculate_button.bind(
            on_release=self.calculate_bmi
        )

        reset_button = Button(
            text="Reset",
            background_color=(0.4, 0.4, 0.4, 1)
        )
        reset_button.bind(
            on_release=self.reset_fields
        )

        button_row.add_widget(calculate_button)
        button_row.add_widget(reset_button)

        self.result_label = MDLabel(
            text="",
            halign="center"
        )

        self.category_label = MDLabel(
            text="",
            halign="center"
        )

        root.add_widget(title)
        root.add_widget(self.weight_input)
        root.add_widget(self.height_input)
        root.add_widget(keypad)
        root.add_widget(button_row)
        root.add_widget(self.result_label)
        root.add_widget(self.category_label)

        return root

    def set_active_weight(self, instance, value):
        if value:
            self.active_input = self.weight_input

    def set_active_height(self, instance, value):
        if value:
            self.active_input = self.height_input

    def keypad_pressed(self, button):
        key = button.text

        if key == "⌫":
            self.active_input.text = self.active_input.text[:-1]

        elif key == "C":
            self.active_input.text = ""

        elif key == ".":
            if "." not in self.active_input.text:
                self.active_input.text += "."

        else:
            self.active_input.text += key

    def reset_fields(self, instance):
        self.weight_input.text = ""
        self.height_input.text = ""
        self.result_label.text = ""
        self.category_label.text = ""

        self.active_input = self.weight_input

    def calculate_bmi(self, instance):
        weight_text = self.weight_input.text.strip()
        height_text = self.height_input.text.strip()

        if not weight_text or not height_text:
            self.result_label.text = "Please fill in both fields."
            self.category_label.text = ""
            return

        try:
            weight = float(weight_text)
            height_cm = float(height_text)

        except ValueError:
            self.result_label.text = "Please enter numbers only."
            self.category_label.text = ""
            return

        if weight <= 0 or height_cm <= 0:
            self.result_label.text = "Please enter positive numbers."
            self.category_label.text = ""
            return

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        self.result_label.text = f"BMI: {bmi:.2f}"

        if bmi < 18.5:
            category = "Underweight"
            color = (1, 0.6, 0, 1)

        elif bmi < 25:
            category = "Normal weight"
            color = (0, 0.7, 0, 1)

        elif bmi < 30:
            category = "Overweight"
            color = (1, 0.6, 0, 1)

        else:
            category = "Obese"
            color = (1, 0, 0, 1)

        self.category_label.text = category
        self.category_label.theme_text_color = "Custom"
        self.category_label.text_color = color


if __name__ == "__main__":
    BMIApp().run()
