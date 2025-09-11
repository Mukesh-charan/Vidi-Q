from manim import *

class BinarySearch(Scene):
    def construct(self):
        # Title
        title = Text("Binary Search").scale(1.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Sorted Array
        array = [2, 5, 7, 8, 11, 12]
        array_mob = VGroup(*[Text(str(x)).scale(0.7) for x in array])
        array_mob.arrange(RIGHT, buff=0.5)
        array_mob.set_color(YELLOW)
        self.play(Write(array_mob))
        self.wait(1)

        # Target Value
        target = 11
        target_text = Text(f"Target: {target}").to_edge(UP)
        self.play(Write(target_text))
        self.wait(1)

        # Search Process
        low = 0
        high = len(array) - 1
        rect = SurroundingRectangle(array_mob[low:high+1], color=BLUE)
        self.play(Create(rect))

        while low <= high:
            mid = (low + high) // 2
            mid_text = Text(f"Mid: {array[mid]}").next_to(array_mob[mid], DOWN)
            self.play(Write(mid_text))
            self.wait(1)

            if array[mid] == target:
                self.play(array_mob[mid].animate.set_color(GREEN))
                self.wait(2)
                break

            elif array[mid] < target:
                low = mid + 1
                rect = SurroundingRectangle(array_mob[low:high+1], color=BLUE)
                self.play(Transform(rect, rect))
                self.wait(1)
                self.play(FadeOut(mid_text))
                
            else:
                high = mid - 1
                rect = SurroundingRectangle(array_mob[low:high+1], color=BLUE)
                self.play(Transform(rect, rect))
                self.wait(1)
                self.play(FadeOut(mid_text))

        self.play(FadeOut(rect), FadeOut(target_text))
        self.wait(1)

        # Conclusion
        conclusion = Text("Binary Search Found!").scale(1.2).set_color(GREEN)
        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion), FadeOut(array_mob))