import streamlit as st
from models import *
import pandas as pd
import numpy as np
from zipfile import ZipFile
from data_visualisation import *
import os
from nn import *
from web3 import Web3
import json

st.set_page_config(page_title="Runtime Error's ML Studio")
w3 = Web3(Web3.HTTPProvider('https://rpc.apothem.network'))
if not w3.is_connected():
    st.error("Failed to connect to Ethereum network!")
    st.stop()
# Smart Contract Address and ABI
contract_address = '0x64e66F74Dc59Dd4B0cA9E6e96a078d96C6fAb499'
account_address = '0x3efA243A455D0B7d06A79F803DAcA81D0707caC3'
private_key = '848be65f1258bb3532c6ba6e8721afd691f4b0fa63588dd3bc975a77313fd9c4'

with open("C:/Users/vundi/OneDrive/Desktop/data science projects/ml studio/ML-Studio/abi.json", 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def store_weights_on_blockchain(weights):
    """
    Store model weights on the blockchain.
    """
    try:
        # Try estimating gas to see if the function call is likely to succeed
        estimated_gas = contract.functions.storeModelWeights(weights).estimateGas({
            'from': account_address
        })
    except Exception as e:
        print(f"Gas estimation failed: {e}")
        estimated_gas = 3000000  # Fallback gas limit if estimation fails

    # Construct a transaction dictionary
    txn_dict = {
        'from': account_address,
        'gas': estimated_gas,
        'gasPrice': w3.eth.gas_price,  # Corrected method to fetch current gas price
        'nonce': w3.eth.get_transaction_count(account_address),
    }

    # Build and sign the transaction
    txn = contract.functions.storeModelWeights(weights).build_transaction(txn_dict)
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)

    # Attempt to send the transaction
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash.hex()
    except Exception as e:
        return f"Transaction failed: {e}"

# Call with correct data type if required by the smart contract, example with a placeholder string
result = store_weights_on_blockchain('Valid input according to your contract')
print(result)





st.title("Machine Learning Studio by Team Runtime Error")
st.subheader("Welcome to the Machine Learning Studio!")
st.markdown('''Build. Train. Deploy. Machine Learning Made Easy.

Drag, drop, and build powerful ML models. Our intuitive studio empowers everyone to harness the power of data.  Start your journey today!''')

# Side bar
st.sidebar.subheader("Setup your Problem Here")
problem_type = st.sidebar.selectbox("Pick your Problem Type", ["Regression", "Classification", "Clustering", "Image Classification"])

if problem_type == "Regression":
    state = 1
elif problem_type == "Classification":
    state = 2
elif problem_type == "Clustering":
    state = 3
else:
    state = 4

if state == 4:
    img_zip_file = st.sidebar.file_uploader("Upload your Dataset", type=['zip'])
else:
    dataset_file = st.sidebar.file_uploader("Upload your Dataset", type=['csv'])
if state != 4:
    if dataset_file:
        st.subheader("Your Dataset:-")
        df = pd.read_csv(dataset_file)
        st.dataframe(df)
        if state == 1 or state == 2:
            target_y = st.sidebar.text_input("Enter the Target Variable Column Name (Leave Blank to use Last Column)")


train_btn = st.sidebar.button("Train")

if st.session_state.get('button') != True:
    st.session_state['button'] = train_btn

if st.session_state['button'] == True:

    comp_table_flag = 1

    if state != 4:
        if (state == 1 or state == 2) and target_y != "":
            cols = list(df.columns.values)
            cols.pop(cols.index(target_y))
            df = df[cols+[target_y]]

        model = Models(df)
        model.clean_and_scale_dataset()

        if state == 1:
            regression_models = ["Linear Regression", "Decision Tree Regression", "SVR", "Ridge Regression", "Lasso Regression",
                                "ElasticNet", "Random Forest Regressor", "Multi-Layer Perceptron", "KNN Regressor", 
                                "Gradient Boosting Regressor"]
            lr = list(model.linear_regression())
            dtr = list(model.dtree_regressor())
            svr = list(model.SVR())
            rr = list(model.ridge_regression())
            lsr = list(model.lasso())
            en = list(model.elasticnet())
            rfr = list(model.random_forest_regressor())
            mlpr = list(model.mlp_regressor())
            knnr = list(model.knn_regressor())
            gbr = list(model.gradient_boost_regressor())
            store_weights_on_blockchain('lr')
            regression_funcs = {
                "Linear Regression": lr[0],
                "Decision Tree Regression": dtr[0],
                "SVR": svr[0],
                "Ridge Regression": rr[0],
                "Lasso Regression": lsr[0],
                "ElasticNet": en[0],
                "Random Forest Regressor": rfr[0],
                "Multi-Layer Perceptron": mlpr[0],
                "KNN Regressor": knnr[0],
                "Gradient Boosting Regressor": gbr[0]
            } 

            metrics = list(lr[1].keys())

            regressors_table = {
                "Linear Regression": list(lr[1].values()),
                "Decision Tree Regression": list(dtr[1].values()),
                "SVR": list(svr[1].values()),
                "Ridge Regression": list(rr[1].values()),
                "Lasso Regression": list(lsr[1].values()),
                "ElasticNet": list(en[1].values()),
                "Random Forest Regressor": list(rfr[1].values()),
                "Multi-Layer Perceptron": list(mlpr[1].values()),
                "KNN Regressor": list(knnr[1].values()),
                "Gradient Boosting Regressor": list(gbr[1].values())
            }
            
            comp_table = pd.DataFrame.from_dict(regressors_table)
            comp_table.index = metrics
            comp_table = comp_table.transpose()

        elif state == 2:
            classification_models = ["SVM", "Logistic Regression", "Decision Tree", "KNN", "Naive Bayes", 
                                    "AdaBoost", "Multi-Layer Perceptron", "Gradient Boosting", "Random Forest"]
            s = list(model.SVM())
            lor = list(model.logistic_regression())
            dt = list(model.dtree_classifier())
            knn = list(model.knn_classifier())
            nb = list(model.naivebayes())
            ab = list(model.adaboost())
            mlp = list(model.mlp())
            gb = list(model.gradient_boost())
            rf = list(model.random_forest_classifier())
            store_weights_on_blockchain(s)
            classification_funcs = {
                "SVM": s[0],
                "Logistic Regression": lor[0],
                "Decision Tree": dt[0],
                "KNN": knn[0],
                "Naive Bayes": nb[0],
                "AdaBoost": ab[0],
                "Multi-Layer Perceptron": mlp[0],
                "Gradient Boosting": gb[0],
                "Random Forest": rf[0]
            }

            metrics = list(s[1].keys())

            classifiers_table = {
                "SVM": list(s[1].values()),
                "Logistic Regression": list(lor[1].values()),
                "Decision Tree": list(dt[1].values()),
                "KNN": list(knn[1].values()),
                "Naive Bayes": list(nb[1].values()),
                "AdaBoost": list(ab[1].values()),
                "Multi-Layer Perceptron": list(mlp[1].values()),
                "Gradient Boosting": list(gb[1].values()),
                "Random Forest": list(rf[1].values())
            }
            comp_table = pd.DataFrame.from_dict(classifiers_table)
            comp_table.index = metrics
            comp_table = comp_table.transpose()
        
        else:
            comp_table_flag = 0
            param_flag = 0
            clustering_models = ["K-Means Clustering", "Agglomerative Clustering", "Density-Based Clustering"]
            num_cluster = st.sidebar.text_input("Enter the Number of Expected Clusters (Leave blank for letting us decide)")
            eps = st.sidebar.text_input("Radius of the Density (Leave blank for letting us decide)")
            min_samples = st.sidebar.text_input("Minimum Number of Samples around the Radius (Leave blank for letting us decide)")

            if st.sidebar.button("Set Parameters"):
                if num_cluster != "":
                    kc = list(model.kmeans(int(num_cluster)))
                    ac = list(model.agglomerative_clustering(int(num_cluster)))
                else:
                    kc = list(model.kmeans(-1))
                    ac = list(model.agglomerative_clustering(-1))
                if eps == "":
                    if min_samples == "":
                        dc = list(model.dbscan())
                    else:
                        dc = list(model.dbscan(min_samples=int(min_samples)))
                else:
                    if min_samples == "":
                        dc = list(model.dbscan(eps=int(eps)))
                    else:
                        dc = list(model.dbscan(eps=int(eps), min_samples=int(min_samples)))

                clustering_funcs = {
                    "K-Means Clustering": kc[0],
                    "Agglomerative Clustering": ac[0],
                    "Density-Based Clustering": dc[0]
                }

                metrics = list(kc[2].keys())

                clustering_table = {
                    "K-Means Clustering": list(kc[2].values()),
                    "Agglomerative Clustering": list(ac[2].values()),
                    "Density-Based Clustering": list(dc[2].values())
                }
                comp_table = pd.DataFrame.from_dict(clustering_table)
                comp_table.index = metrics
                comp_table = comp_table.transpose()
                comp_table_flag = 1
    
    else:
        # comp_table_flag = 0
        # with ZipFile(img_zip_file, "r") as zf:
        #     zf.extractall("image_data/")
        # sub_list = os.listdir("image_data/")

        
        # if len(sub_list) > 1:
        #     nn = NeuralNetwork("image_data/")
        # else:
        #     nn = NeuralNetwork(f"image_data/{sub_list[0]}/")
        # nn.make_train_val_dirs()
        # nn.create_dataset()
        # nn.train_val_gens()

        # nn.model_vgg()
        # nn.model_mobilenetv2()
        # nn.resnet()


        # for root, dirs, files in os.walk("image_data/", topdown=False):
        #     for file in files:
        #         os.remove(os.path.join(root, file))
        #     for dir in dirs:
        #         os.rmdir(os.path.join(root, dir))
        comp_table_flag = 0
        st.subheader("We are extremely Sorry!")
        st.markdown("We are currently working on implementing this feature...Check back soon!")

    if comp_table_flag:
        st.subheader("Comparision Table")
        st.dataframe(comp_table)
        if state == 1:
            main(state=state,comp_table=comp_table,df = df,model_names=regression_models)
        elif state == 2:
            main(state=state,comp_table=comp_table,df=df,model_names=classification_models)
        else:
            main(state=state,comp_table=comp_table,df=df,model_names=clustering_models,models = clustering_funcs)