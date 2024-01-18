
AA=(`oc get pod -n=default --output=jsonpath={.items..metadata.name}`)



for ns in "${AA[@]}"; do
    # oc logs $ns -c selenium | tail -n 1
    oc logs $ns -c selenium | grep \>, | cut -c4-
done

