# Web-Locator-Tools (PLaywright with TS)

* Run main.py or compile into an exe and run using pyinstaller
* Copy html blocks to display locators, locators are copied in priority order
* If copied locator is bad, click the copy button on another locator

> Main.py can be edited to change the priority order by editing this line:
> ```
> self.priority_attributes = ["for", "data-test-id", "data-testid", "id", "name", "title", "aria-label",
                                    "placeholder", "value", "data-cy", "class"]
> ```

## FAQ
* How do I copy html while the app is running?
> Click the pause button OR copy the text twice (If the read clipboard is the same as the previous it is ignored)
