from manim import *

class LinearRegression(Scene):
    def construct(self):
        # Data points
        points = [
            (1, 2), (2, 3), (3, 5), (4, 4), (5, 6), (6, 7)
        ]
        dots = VGroup(*[Dot(np.array([x, y, 0])) for x, y in points])
        self.play(Create(dots))
        self.wait(1)

        # Scatter plot label
        scatter_label = Tex("Scatter Plot").to_edge(UP)
        self.play(Write(scatter_label))
        self.wait(1)

        # Best fit line
        x_coords = [x for x, y in points]
        y_coords = [y for x, y in points]
        A = np.vstack([x_coords, np.ones(len(x_coords))]).T
        m, c = np.linalg.lstsq(A, y_coords, rcond=None)[0]
        line_func = lambda x: m * x + c
        line = FunctionGraph(line_func, x_range=[0.5, 6.5], color=YELLOW)
        self.play(Create(line))
        self.wait(1)

        # Line equation
        equation = MathTex("y = mx + c").next_to(line, UP)
        self.play(Write(equation))
        self.wait(1)

        # m and c values
        m_val = MathTex("m =", str(round(m, 2))).next_to(equation, DOWN)
        c_val = MathTex("c =", str(round(c, 2))).next_to(m_val, RIGHT)

        self.play(Write(m_val), Write(c_val))
        self.wait(2)


        # Explanation
        explanation = Tex("This line minimizes the distance to all points").next_to(equation, DOWN, buff=1)
        self.play(Write(explanation))
        self.wait(2)

        #Prediction
        x_new = 7
        y_new = line_func(x_new)
        new_point = Dot(np.array([x_new,y_new,0]), color=RED)
        prediction_text = Tex(f"Prediction for x={x_new}: y={y_new:.2f}").next_to(explanation, DOWN)
        self.play(Create(new_point),Write(prediction_text))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])