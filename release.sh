if !($(git rev-parse --abbrev-ref HEAD | grep -q 'release/*')); then
  echo "Must be on release branch to create release."
  exit 1
fi

# get release type
case $1 in

  major | minor | patch)
    RELEASE_TYPE=$1
    ;;

  *)
    echo "Please specify release type of 'major', 'minor', or 'patch'"
    exit 1
    ;;
esac

echo "Starting '$RELEASE_TYPE' release."
git pull

# get current version
CURRENT_VERSION="$(cat setup.py | grep version | grep -oP '[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}')"
echo -e "\nCurrent version: $CURRENT_VERSION"

IFS='.' read -r -a VERSION_DATA <<< "$CURRENT_VERSION"
CURRENT_MAJOR="${VERSION_DATA[0]}"
CURRENT_MINOR="${VERSION_DATA[1]}"
CURRENT_PATCH="${VERSION_DATA[2]}"

# update version based on release type
case $RELEASE_TYPE in

  'major')
    NEW_MAJOR=$((CURRENT_MAJOR+1))
    NEW_MINOR=0
    NEW_PATCH=0
    ;;

  'minor')
    NEW_MAJOR=$CURRENT_MAJOR
    NEW_MINOR=$((CURRENT_MINOR+1))
    NEW_PATCH=0
    ;;

  'patch')
    NEW_MAJOR=$CURRENT_MAJOR
    NEW_MINOR=$CURRENT_MINOR
    NEW_PATCH=$((CURRENT_PATCH+1))
    ;;
esac

NEW_VERSION="$NEW_MAJOR.$NEW_MINOR.$NEW_PATCH"

echo "New Version: $NEW_VERSION"

# update files with new version
sed -i "s/version='$CURRENT_VERSION'/version='$NEW_VERSION'/g" setup.py
sed -i "s/version-$CURRENT_VERSION-blue/version-$NEW_VERSION-blue/g" README.MD

# push changes
git add setup.py README.MD
git commit -m "update version to $NEW_VERSION"
git push

# Create new version tag and update latest tag
git tag -d latest
git push --delete origin latest

git tag "v$NEW_VERSION"
git tag latest
git push origin --tags