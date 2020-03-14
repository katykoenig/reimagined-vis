# v_a11y_lint

## What is v_a11y_lint?

v_a11y_lint is a lint software to flag issues regarding accessibility in data visualizations. Specifically, our software flags issues in font size, text color, color scales and title to ensure that the data visualization created is accessible to people with low vision. Where applicable, we use WCAG guidelines, research regarding perceivable colors and accepted best practices to create these rules, but much research is still needed to create a standardization of guidelines for accessible data visualizations.

v_a11y_lint lints charts created in Python's Altair data visualization library. While Altair is not Python's most popular data visualization library, as it is the Python library that follows a grammer of graphics, we hope our linter can serve as a foundation for accessible plot linters in other grammar of graphics libraries, like vega/vega-lite and ggplot. Additionally, we hope the v_a11y_lint helps to make accessible plots the norm through making it easier to create accessible data vis.

## How do I make my data visualizations accessible using v_a11y_lint?
	1. Make your chart object, using Altair.
		* You can set your global theme yourself or use the default theme in Altair.
		* Assign your chart object a name (not just render it).
	2. Pass your chart object into v_a11y_lint.
		* After downloading v_a11y_lint and it's dependencies, run `v_a11ylint.run_lint(my_chart_obj)` or if you want more information regarding the accessibility issues, run `v_a11ylint.run_lint(my_chart_obj, verbose=true)`
		* Read what is not accessible with your vis.
	3. Update your chart object, or global theme configurations, to address issues printed.
	4. Rerun v_a11y_lint and repeat step 3 if necessary until you get the message:
		```'Visualization is Accessible!'```
	5. Save your cool new accessible data visualization using a high dpi, and proceed as normal!

