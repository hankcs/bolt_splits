# bolt_splits
Split Broad Operational Language Translation corpus into train/dev/test set.

The pseudo-code for splitting goes as follows:

```
For files in each genre:
  For files in each ext:
    For files in each length of filename:
      Sort files by filename
      Split files to trn, dev, tst with 8:1:1 ratio
```

