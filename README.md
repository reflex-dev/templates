# Reflex Templates

A repository of Reflex template apps.


# How to deploy templates
If this a template for build, you must include a `preview.png` or `preview.webp` which will be used as the preview image.

To get a url for your app, you must make a release with a valid reflex version. This can be difficult since part of the reflex opensource deployment pipeline is to create a release for every version to make sure that all templates work with it. So to get around this you must do a few things:
## Crafting a new release
- Delete a release
- Delete the relating tag
- Recreate the deleted release and tag 

**NOTE:** Ideally do not delete the most recent release as to lessen the impact of this. ALSO if you are not deleting the most recent DO NOT mark the release as latest

**Be warned that upon deleting the release on this repo will remove all the templates for anyone using that version of reflex until the release is recreated and all jobs related to the release are complete.**

## Get deployed URL
One of the jobs from a release is to deploy the template. This will result in a url that anyone can go to, to view the template. You can find this either in the action logs or by searching for it in the Templates project in Cloud.

## Updating templates json
Once you have completed all of the above steps you can now accurately update the `templates.json`
Add a new/update the object in this file to have all the accurate information required.

## Getting updated packages
Now that you have an accurate `templates.json` in main you can now craft a new phony release. This release unlike the other does not need to be of a real reflex version. It can, but weather it is or is not will not have any impact on the remaining steps.
Once you have drafted a new release, and all the actions have finished (the deploy will fail if this is a phony release version).
Then you can either kick off the deploy job on templates for `Publish Templates` or you can kick off the sister job in the build repo. 



