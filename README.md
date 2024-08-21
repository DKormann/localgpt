## lcoal gpt client in terminal 

```python
python localgpt.py <OPENAI_API_KEY>
```

recommended to add a line to your bashrc:
```bash
alias g='p ~/localgpt/localgpt.py $OPENAI_API_KEY
```


than you can prompt gpt from terminal/ chat/ execute his code
```
➜  localgpt git:(master) g how to get remote 
Bot: To retrieve the remote URLs for your git repository, you can use the following command in your terminal:

\```bash
git remote -v
\```

This command will show you a list of remotes along with their fetch and push URLs. Let me know if you need further help!
You: run
Bot: Running code...

origin	git@github.com:DKormann/localgpt.git (fetch)
origin	git@github.com:DKormann/localgpt.git (push)
You:     
```
