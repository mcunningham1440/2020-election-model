# What is NeoSlim?
NeoSlim is a Python program I wrote as a hobby project back in the spring of 2020 to predict the results of the November US presidential election. I was dabbling in the prediction market PredictIt as a way to kill time during the pandemic and this gave me the chance to have some fun playing Nate Silver.

# How does it work?
NeoSlim creates a probability distribution of election results by running 100,000 random simulations. First, the state and national polling data **at the time the model is run** are used to predict the state of the polls **on Election Day**, which are then used to predict the **actual results**.

Breaking this two-step process into its constituent parts makes it simpler to tackle, since there is a complex relationship between state and national polls, how they change over time, and how closely they predict the actual results on Election Day. The details of how this is done are documented in the code.

# Where does the name come from?
The name just means new model, slimmed down. I had previously started on a much more ambitious and detailed program, but realized that its complexity was getting out of hand and likely wouldn't increase my accuracy much. I started fresh with this version and was satisfied with its performance.
