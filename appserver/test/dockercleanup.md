# Kill all running containers

```
docker kill $(docker ps -q)
```

# Delete all stopped containers (including data-only containers)

```
docker rm $(docker ps -a -q)
```

# Delete all 'untagged/dangling' (<none>) images

```
docker rmi $(docker images -q -f dangling=true)
```

# Delete ALL images

```
docker rmi $(docker images -q)
```

## It might also be useful to create bash aliases for these commands, for example:

```
# ~/.bash_aliases

# Kill all running containers.
alias dockerkillall='docker kill $(docker ps -q)'

# Delete all stopped containers.
alias dockercleanc='printf "\n>>> Deleting stopped containers\n\n" && docker rm $(docker ps -a -q)'

# Delete all untagged images.
alias dockercleani='printf "\n>>> Deleting untagged images\n\n" && docker rmi $(docker images -q -f dangling=true)'

# Delete all stopped containers and untagged images.
alias dockerclean='dockercleanc || true && dockercleani'
```
