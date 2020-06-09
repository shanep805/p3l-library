# p3l-library
Examples for Paperless Parts Pricing Language (P3L) programs

P3L is a mini-language based on Python 3. It was created to make it very easy to express your pricing with small snippets of code.
P3L extends python by adding global objects and functions and removes some other Python functionality for security and performance.

We have developed P3L to be very easy to learn and use for users comfortable with spreadsheets.
You do not need to have experience in software development to be able to write or customize a P3L pricing program.

# Processes and Operations
The Paperless Parts platform centers on quotes. Quotes contain quote items, quote items contain one or more components, and components are parts you will manufacture, assemble, or purchase (e.g. hardware).
Each component is manufactured using a single process. Some shops offer one process, while others may offer many different processes. The process determines which steps a part must go through before a shop can deliver a finished product.
In Paperless Parts, each step of this process is called an operation. P3L runs at the operation level to estimate the cost and lead time required to perform that operation for a particular quantity.

There are many inputs to a P3L program. The part specifications (like dimensions, weight, material, etc.) and make quantity are some examples of things you can interact with.
The output of an operation P3L program is the price (in dollars) and lead time (in business days) required to produce the specified quantity of part.

When pricing a component with multiple operations and quantities, a P3L program will be executed for each operation along each quantity break. The outputs of the operations then sum across the component.
If the quote item has more than one component (for assembly files), the totals will then sum across all components associated with a quote item.

# Resources
Visit the resources page at https://help.paperlessparts.com/ for more detailed information on how to work with P3L. This repo is meant to be a resource for many examples for you to use/start from in your profiles.
